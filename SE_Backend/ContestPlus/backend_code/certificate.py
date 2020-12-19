from PIL import Image
from SE_Backend import settings

def apiCertificationGet(request):
    image=Image.open(str(settings.BASE_DIR)+"/CertificationModel/certification_model.png")


    image.show()
    return


def apiCertificationVerify(request):

    return
