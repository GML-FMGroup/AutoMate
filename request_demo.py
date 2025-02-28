import asyncio
import websockets
import json

async def send_request():
    url = "ws://172.16.8.34:8000/chat"  # WebSocket 服务地址
    async with websockets.connect(url) as websocket:
        infro = {
            "token": 111111
        }
        await websocket.send(json.dumps(infro))

        # data = {
        #     "agent_type": "workflow",
        #     "planner_model": "",
        #     "planner_provider": "",
        #     "planner_api_key": "",
        #     "planner_base_url": "",
        #     "executor_model": "qwen2.5-vl-7b-instruct",
        #     "executor_provider": "dashscope",
        #     "executor_api_key": "",
        #     "executor_base_url": "",
        #     "user_query": "",
        #     "user_tasks": ["search 'https://www.bilibili.com/' in search box", "search 'python' in bilibili search box", "click on the first video"],
        # }

        data = {
            "agent_type": "planner",
            "planner_model": "gpt-4o",
            "planner_provider": "openai",
            "planner_api_key": "",
            "planner_base_url": "",
            "executor_model": "qwen2.5-vl-7b-instruct",
            "executor_provider": "dashscope",
            "executor_api_key": "",
            "executor_base_url": "",
            "user_query": "I want to watch python related videos on Bilibili",
            "user_tasks": [],
        }
        await websocket.send(json.dumps(data))

        while True:
            response = await websocket.recv()

            # 判断是否是二进制数据
            if isinstance(response, bytes):
                # 这里可以保存为图片或处理二进制数据
                with open("received_image.jpg", "wb") as image_file:
                    image_file.write(response)

            elif isinstance(response, str):
                # 如果是字符串，则认为是 JSON 数据
                try:
                    response = json.loads(response)  # 将字符串解析为 JSON 对象
                    print("Received JSON data:", response)
                    # 在这里处理你收到的 JSON 数据
                except json.JSONDecodeError:
                    print("Failed to decode JSON data")

                if response["message"] == "Processing complete":
                    break
                
                await asyncio.sleep(1)


# 运行客户端
asyncio.get_event_loop().run_until_complete(send_request())


