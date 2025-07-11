import duckduckgo_search, logging, time, random
from google.adk.tools import ToolContext
from google.genai.types import Part

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def knowledge_inter_tool(tool_context: ToolContext) -> dict:
    filename = "knowledge_inter_text"
    query = tool_context.state["user_query"]
    context_text = ""

    try:
        # 尝试使用 DuckDuckGo 搜索（带重试机制）
        for attempt in range(3):
            try:
                results = list(duckduckgo_search.DDGS().text(
                    query,
                    region="wt-wt",  # 使用国际版更稳定
                    safesearch="off",
                    max_results=5
                ))

                # 提取有效内容
                valid_results = [res.get("body", "") for res in results if "body" in res and res["body"].strip()]

                if valid_results:
                    context_text = "\n\n".join(valid_results)
                    logger.info(f"DuckDuckGo搜索成功，获取到{len(valid_results)}条结果")
                    break
                else:
                    logger.warning(f"DuckDuckGo搜索返回空结果（尝试 {attempt + 1}/3）")

            except Exception as e:
                logger.warning(f"DuckDuckGo搜索异常（尝试 {attempt + 1}/3）: {str(e)}")

            # 指数退避重试
            if attempt < 2:
                sleep_time = random.uniform(0.5, 2.0) * (2 ** attempt)
                time.sleep(sleep_time)

        # 如果DuckDuckGo失败，尝试使用备用搜索方案
        if not context_text:
            logger.info("尝试使用备用搜索方案")
            context_text = fallback_search(query)

        # 保存结果
        version = tool_context.save_artifact(
            filename=filename,
            artifact=Part(text=context_text)
        )

        logger.info("Saved artifact %s, ver %i", filename, version)
        return {"status": "OK", "results_count": len(context_text.split("\n\n"))}

    except Exception as err:
        logger.error("搜索失败: %s", err, exc_info=True)
        return {"status": "ERROR", "error_message": str(err)}


def fallback_search(query: str) -> str:
    """备用搜索方案"""
    try:
        # 尝试使用DuckDuckGo的新闻搜索作为备用
        with duckduckgo_search.DDGS() as ddgs:
            results = ddgs.news(
                query,
                region="wt-wt",
                safesearch="off",
                max_results=3
            )
            return "\n\n".join([res.get("body", res.get("title", "")) for res in results])

    except Exception as e:
        logger.error(f"备用搜索也失败: {str(e)}")
        # 最终返回一个友好的错误信息
        return (f"无法获取实时搜索结果。建议直接访问搜索引擎查询: '{query}'。"
                "常见原因：网络问题、服务暂时不可用或搜索限制。")