from PIL import Image
from PIL import ImageDraw
from SE_Backend import settings

def apiCertificationGet(request):
    image=Image.open(str(settings.BASE_DIR)+"/CertificationModel/certification_model.png")
    draw=ImageDraw.Draw(image)
    draw.text((400,400),u"闷声发大财",font='',fill='white')
    image.show()
    return


def apiCertificationVerify(request):

    return
