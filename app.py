import streamlit as st
import PIL.Image
import PIL.ImageFilter
import io
import json
from src.bbox_annotation import st_labelstudio
from base64 import b64encode, decode

st.set_page_config(layout='wide')
st.title("Label Studio")


@st.cache
def url_encoder(image):
    img = PIL.Image.open(image)
    blurred_image = img.filter(PIL.ImageFilter.GaussianBlur(5))

    url = f'data:image/jpg;base64, ' + pillow_image_to_base64_string(blurred_image)

    return url or "None"


def pillow_image_to_base64_string(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")

    return b64encode(buffered.getvalue()).decode("utf-8")


with st.sidebar.container():
    st.markdown("""## Batch Image Upload """)

    uploaded_files_multi = st.file_uploader(
        label="Upload Image", type=['jpg', "png", "jpeg"], accept_multiple_files=True, key=2)

if uploaded_files_multi:
    image_name = {}
    image_list = []
    i = 0

    for image in uploaded_files_multi:
        image_name[image.name] = i
        image_list.append(image.name)
        i += 1
    image_sel = st.sidebar.selectbox(
        "Select image", image_list)

    data_url = url_encoder(uploaded_files_multi[image_name[image_sel]])

else:
    data_url = ""

pass


config = """
      <View>
        <View style="padding: 25px; box-shadow: 2px 2px 8px #AAA;">
          <Image name="img" value="$image" width="100%" maxWidth="100%"></Image>
        </View>
        <RectangleLabels name="tag" toName="img">
          <Label value="Name"></Label>
          <Label value="FName"></Label>
          <Label value="Gender"></Label>
          <Label value="CNIC"></Label>
          <Label value="DOB"></Label>
        </RectangleLabels>
      </View>
    """

interfaces = [
                 "controls",
                 "panel",
                 "side-column",
             ],

user = {
           'pk': 1,
           'firstName': "Minaam",
           'lastName': "Awan"
       },

task = {
    'completions': [],
    'predictions': [],
    'id': 1,
    'data': {
        'image': f'{data_url}'
    }
}

results_raw = st_labelstudio(config, interfaces, user, task)

if results_raw is not None:
    areas = [v for k, v in results_raw['areas'].items()]

    results = []
    for a in areas:
        results.append({'id': a['id'], 'x': a['x'], 'y': a['y'], 'width': a['width'],
                        'height': a['height'], 'label': a['results'][0]['value']['rectanglelabels'][0]})

    with open('Annotation.json', 'w') as outfile:
        json.dump(results, outfile)

    st.table(results)
