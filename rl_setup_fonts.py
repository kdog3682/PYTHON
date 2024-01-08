from utils import *
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BaseFonts = [
    {"path": "Hanyi Senti Rubber.ttf", "alias": "HanyiSentiRubber", "tag": "Playful"},
    {"path": "HanyiSentyBubbleTea.ttf", "alias": "HanyiSentyBubbleTea", "tag": "Fun"},
    {"path": "LiuJianMaoCao-Regular.ttf", "alias": "LiuJianMaoCaoRegular", "tag": "chinese"},
    {"path": "LongCang-Regular.ttf", "alias": "LongCangRegular", "tag": "chinese"},
    {"path": "Material Icons Round.woff2", "alias": "MaterialIconsRound", "tag": "Modern"},
    {"path": "Material Icons Sharp.woff2", "alias": "MaterialIconsSharp", "tag": "Crisp"},
    {"path": "Material Icons.woff2", "alias": "MaterialIcons", "tag": "Contemporary"},
    {"path": "Material Symbols Outlined.woff2", "alias": "MaterialSymbolsOutlined", "tag": "Outlined"},
    {"path": "MaterialIconsOutlined-Regular.otf", "alias": "MaterialIconsOutlinedRegular", "tag": "Sleek"},
    {"path": "NotoColorEmoji.ttf", "alias": "NotoColorEmoji", "tag": "Colorful"},
    {"path": "NotoEmoji-VariableFont_wght.ttf", "alias": "NotoEmojiVariableFontWght", "tag": "Expressive"},
    {"path": "NotoSansSC-Black.otf", "alias": "NotoSansSCBlack", "tag": "Bold"},
    {"path": "NotoSansSC-Bold.otf", "alias": "NotoSansSCBold", "tag": "Strong"},
    {"path": "NotoSansSC-Light.otf", "alias": "NotoSansSCLight", "tag": "Delicate"},
    {"path": "NotoSansSC-Medium.otf", "alias": "NotoSansSCMedium", "tag": "Medium"},
    {"path": "NotoSansSC-Regular.otf", "alias": "NotoSansSCRegular", "tag": "Normal"},
    {"path": "NotoSansSC-Thin.otf", "alias": "NotoSansSCThin", "tag": "Thin"},
    {"path": "NotoSerifSC-Black.otf", "alias": "NotoSerifSCBlack", "tag": "Elegant"},
    {"path": "NotoSerifSC-Bold.otf", "alias": "NotoSerifSCBold", "tag": "Formal"},
    {"path": "NotoSerifSC-ExtraLight.otf", "alias": "NotoSerifSCExtraLight", "tag": "Light"},
    {"path": "NotoSerifSC-Light.otf", "alias": "NotoSerifSCLight", "tag": "Soft"},
    {"path": "NotoSerifSC-Medium.otf", "alias": "NotoSerifSCMedium", "tag": "Balanced"},
    {"path": "NotoSerifSC-Regular.otf", "alias": "NotoSerifSCRegular", "tag": "Classic"},
    {"path": "NotoSerifSC-SemiBold.otf", "alias": "NotoSerifSCSemiBold", "tag": "Impactful"},
    {"path": "Sohne-Halbfett.otf", "alias": "SohneHalbfett", "tag": "Stylish"},
    {"path": "SourceHanSerifSC-Bold.otf", "alias": "SourceHanSerifSCBold", "tag": "Authoritative"},
    {"path": "SourceHanSerifSC-Regular.otf", "alias": "SourceHanSerifSCRegular", "tag": "Serious"},
    {"path": "ZCOOLKuaiLe-Regular.ttf", "alias": "ZCOOLKuaiLeRegular", "tag": "Cheerful"},
    {"path": "ZhiMangXing-Regular.ttf", "alias": "ZhiMangXingRegular", "tag": "Dynamic"},
    {"path": "casual.ttf", "alias": "Casual", "tag": "chinese"},
    {"path": "jason.ttf", "alias": "Jason", "tag": "chinese"},
    {"path": "material-icons.woff2", "alias": "MaterialIcons", "tag": "Iconic"},
    {"path": "minion-bold-italic.ttf", "alias": "MinionBoldItalic", "tag": "Emphasized"},
    {"path": "minion-bold.ttf", "alias": "MinionBold", "tag": "math"},
    {"path": "minion-italic.ttf", "alias": "MinionItalic", "tag": "math"},
    {"path": "minion.ttf", "alias": "Minion", "tag": "math"},
    {"path": "symbola.otf", "alias": "Symbola", "tag": "math"}
]


def register_fonts(key):
    fonts = filter(BaseFonts, {"tag": key})
    for font in fonts:
        path = "/home/kdog3682/2023/fonts/" + font.get("path")
        pdfmetrics.registerFont(TTFont(font.get("name"), path))
