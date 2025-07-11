# service_agent

##### 运行：

1. 修改env中的GOOGLE_API_KEY

2. 上传本地知识库中的文件到chroma数据库
   
   ```bash
   cd ./service_agent/service_agent/agent/data
   python upload_file_to_chroma.py
   ```

3. 回到.env文件相同目录
   
   ```bash
   cd ../..
   ```

4. 本地测试
   
   ```bash
   akd web
   ```
   
   打开本地网页：(localhost:8000)测试
