import csv, logging, os
from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def append_complaint_tool(
    tool_context: ToolContext
) -> dict:
    name = tool_context.state["user_name"]
    contact = tool_context.state["user_phone"]
    issue = tool_context.state["user_complaint"]
    request = tool_context.state["user_request"]
    filename = "complaints.csv"
    row = f"{name},{contact},{issue},{request}"

    try:
        csv_path = "./service_agent/data/complaints.csv"
        file_exists = os.path.exists(csv_path)

        with open(csv_path, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            # 若文件不存在，写入标题行
            if not file_exists:
                header = ["名字","联系方式","问题"," 需求"]
                writer.writerow(header)
            # 追加数据行
            writer.writerow(row.split(','))
        logger.debug("Appended to %s: %s", filename, row.strip())
        return {"status": "OK"}
    except Exception as err:
        logger.error("Failed to append complaint to %s: %s", filename, err)
        return {"status": "ERROR", "error_message": str(err)}
