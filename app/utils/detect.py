from ultralytics import YOLO
import traceback
import os


def detect(model_path, image_path, user_id, output_dir=None):
    try:
        model = YOLO(model_path)

        # 确保输出目录存在
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # 运行检测并指定保存路径
        results = model.predict(
            source=image_path,
            save=True,
            project=output_dir if output_dir else None,
            name=str(user_id),  # 空字符串表示不创建子目录
            exist_ok=True  # 允许覆盖现有文件
        )

        detection_results = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                detection_results.append({
                    'bbox': box.xyxy[0].tolist(),
                    'confidence': float(box.conf),
                    'class_id': int(box.cls),
                    'class_name': model.names[int(box.cls)]
                })
        return detection_results

    except Exception as e:
        print(f"检测错误: {str(e)}")
        print(traceback.format_exc())
        raise


if __name__ == '__main__':
    # 指定保存路径
    custom_save_path = r"D:\Projects\backend\detect"

    results = detect(
        model_path=r"D:\Projects\PythonProject\runs\detect\insect_detection_optimized\weights\best.pt",
        image_path=r"D:\Projects\PythonProject\972.jpg",
        output_dir=custom_save_path,
        user_id=1
    )

    for res in results:
        print(res)

    print(f"\n结果已保存到: {custom_save_path}")