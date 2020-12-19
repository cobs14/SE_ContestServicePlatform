from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from ContestPlus.backend_code import secure
import qrcode
from SE_Backend import settings


def apiCertificationGet(request):
    image = Image.open(str(settings.BASE_DIR) + "/CertificationModel/certification_model.png")
    draw = ImageDraw.Draw(image)


    name_text = "李云轩" + ":"
    contest_text_part1 = "恭喜你在" + "清华大学" + "举办的"
    contest_text_part2 = "第一届厨艺大赛" + "中获得"
    award_text = "最佳创意奖"
    sponsor_text = "清华大学"
    time_text = "2020年12月20日"
    qrcode_text = "扫描二维码验证："
    host_name = "http://127.0.0.1:8080/certificate/"

    name_position = (380 - 36 * (len(name_text) - 1), 565)
    name_font = ImageFont.truetype(r'C:\Windows\Fonts\STXINWEI.TTF', 72)
    draw.text(name_position, name_text, font=name_font, fill='white')

    contest_position_part1 = (1000 - 25 * (len(contest_text_part1)), 640)
    contest_font_part1 = ImageFont.truetype(r'C:\Windows\Fonts\STZHONGS.TTF', 50)
    draw.text(contest_position_part1, contest_text_part1, font=contest_font_part1, fill='white')

    contest_position_part2 = (1000 - 25 * (len(contest_text_part2)), 710)
    contest_font_part2 = ImageFont.truetype(r'C:\Windows\Fonts\STZHONGS.TTF', 50)
    draw.text(contest_position_part2, contest_text_part2, font=contest_font_part2, fill='white')

    award_position = (1000 - 50 * (len(award_text)), 780)
    award_font = ImageFont.truetype(r'C:\Windows\Fonts\STZHONGS.TTF', 100)
    draw.text(award_position, award_text, font=award_font, fill='white')

    sponsor_position = (1600 - 18 * (len(sponsor_text)), 1100)
    sponsor_font = ImageFont.truetype(r'C:\Windows\Fonts\STZHONGS.TTF', 36)
    draw.text(sponsor_position, sponsor_text, font=sponsor_font, fill='white')

    time_position = (1600 - 18 * (len(time_text) - 3), 1150)
    time_font = ImageFont.truetype(r'C:\Windows\Fonts\STZHONGS.TTF', 36)
    draw.text(time_position, time_text, font=time_font, fill='white')

    qrcode_position = (1005 - 18 * (len(qrcode_text)), 950)
    qrcode_font = ImageFont.truetype(r'C:\Windows\Fonts\STZHONGS.TTF', 36)
    draw.text(qrcode_position, qrcode_text, font=qrcode_font, fill='white')
    qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4, )
    qr.add_data(host_name+secure.random_str(32))
    qr.make(fit=True)
    qr_img = qr.make_image()
    qr_img = qr_img.resize((200, 200))
    image.paste(qr_img, (900, 1020))

    image.save(str(settings.BASE_DIR) + "/file/needPermission/certificate/"+participation.id+".png")
    image.show()
    return


def apiCertificationVerify(request):

    return
