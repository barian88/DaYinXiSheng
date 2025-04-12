
from flask import Flask, request, render_template, jsonify, send_from_directory
import onnxruntime as ort
import torchvision.transforms as transforms
from PIL import Image
import io

app = Flask(__name__)


# 加载模型
model_path = 'checkpoint_019.onnx'
sess = ort.InferenceSession(model_path)
# 获取模型的输入信息
input_name = sess.get_inputs()[0].name

# 定义转换操作，与你的数据集类中的相同
transform = transforms.Compose([
    # transforms.ToPILImage(),  web应用中使用PIL读取图片，不需要这一步
    # transforms.Resize((224, 224)),  # 假设你的模型需要224x224大小的图片
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.59685254, 0.59685254, 0.59685254], std=[0.16043035, 0.16043035, 0.16043035])
])

def prepare_image(img_bytes):

    # 使用Pillow加载图像
    image = Image.open(io.BytesIO(img_bytes))

    # 如果图像是灰度图，需要转换为RGB
    if image.mode == 'L':
        image = image.convert('RGB')

    # 应用转换
    image = transform(image)

    # 添加一个批次维度，因为模型预期的输入通常是一个批次的数据
    image = image.unsqueeze(0)  # 将shape从[C, H, W]改为[1, C, H, W]

    # 转换为numpy数组
    image = image.numpy()

    return image



# base_dir = r'E:\Projects\src_to_implement'
# image_path = os.path.join(base_dir, 'images/cell2241.png')
# image_tensor = prepare_image(image_path)

# # 运行模型
# outputs = sess.run(None, {input_name: image_tensor})
#
# # 输出是一个列表，每个元素对应一个输出
# print(outputs)

@app.route('/', methods=['GET', 'POST'])
def upload_predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file:
            image_bytes = file.read()
            image_tensor = prepare_image(image_bytes)
            outputs = sess.run(None, {input_name: image_tensor})
            # 处理输出以显示预测结果
            prediction = outputs[0][0]
            # print(prediction)
            # q: prediction包含两个值，分别是两个类别的概率
            result = {
                'class_0': format(float(prediction[0]), '.3f'),
                'class_1': format(float(prediction[1]), '.3f')
            }
            return jsonify(result)

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)