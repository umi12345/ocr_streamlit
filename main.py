# ライブラリのインポート
import streamlit as st
from PIL import Image

#サイドバーに表示させる
st.sidebar.header('画像から文字起こし')
# ファイルアップロード
upload_file = st.sidebar.file_uploader('↓ファイルをアップロードしてください',type=['png', 'jpg', 'gif', 'jpeg'])


# メイン画面
if upload_file is not None:
    image = Image.open(upload_file).convert('RGB')
    # st.write(image.width)
    # st.write(image.height)
    # st.image(image, use_column_width=True)
    
    # 画像サイズを格納
    lower = image.width
    upper = image.height

    # サイドバーに追加
    #  # 読み取り範囲の指定
    st.sidebar.write('↓画像の読み取り範囲を指定してください')
    # x座標（横軸）
    x1, x2 = st.sidebar.slider('横軸', 0.0, float(lower), (10.0, float(lower-10.0)))
    st.sidebar.write('左,右:',(x1, x2))
    # y座標（縦軸）
    y1, y2 = st.sidebar.slider('縦軸', 0.0, float(upper), (10.0, float(upper-10.0)))
    st.sidebar.write('上,下:',(y1, y2))


    image_crop = image.crop((x1, y1, x2, y2)).resize((1024,768))
    image_crop.save('sample.png')
    # st.write(image_crop.width)
    # st.write(image_crop.height)
    st.image(image_crop, use_column_width=True)


    # VISION API
    # サイドバーにボタンを追加
    if st.sidebar.button('文字起こし！'):

        #モジュールのインポート 
        from google.cloud import vision
        from google.oauth2 import service_account
        # jsonの読み込み
        credentials = service_account.Credentials.from_service_account_info(["gcp_service_account]")
        client = vision.ImageAnnotatorClient(credentials=credentials)

        # 画像の読み込み
        with open('sample.png', 'rb') as image_file:
            content = image_file.read()
            v_image = vision.Image(content=content)
            response = client.document_text_detection(image=v_image)
            texts = response.full_text_annotation.text
            st.write(texts)


                