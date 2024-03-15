import cv2

# 通过摄像头捕获视频
cap = cv2.VideoCapture(0)  # 0 表示默认摄像头

# 定义视频编码器并创建 VideoWriter 对象
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 使用 XVID 编码器
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))  # 输出文件名、编码器、帧率、分辨率

while True:
    # 读取一帧
    ret, frame = cap.read()

    if not ret:
        break  # 如果读取失败，退出循环

    # 将帧写入输出视频文件
    out.write(frame)

    # 显示帧
    cv2.imshow('Frame', frame)

    # 按 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
out.release()
cv2.destroyAllWindows()
