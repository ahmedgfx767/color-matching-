import streamlit as st
from PIL import Image
import colorsys
import io

st.set_page_config(page_title="ColorPop | Color Studio", page_icon="🎨", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:linear-gradient(135deg,#faf8ff 0%,#fff7fb 55%,#fffaf0 100%);}
.hero {padding:1.7rem 2rem;border-radius:24px;background:linear-gradient(115deg,#eee9ff,#fff0f7,#fff7e8);margin-bottom:1.2rem;}
.hero h1 {font-size:2.7rem;line-height:1.12;color:#282342;margin:0;}
.hero p {color:#716b89;font-size:1rem;margin-bottom:0.2rem;}
.pill {display:inline-block;padding:5px 10px;border-radius:20px;background:#e6deff;color:#6849ef;font-size:.75rem;font-weight:800;letter-spacing:1px;margin-bottom:12px;}
div[data-testid="stColorPicker"] {padding:.2rem 0;}
div[data-testid="stMetric"] {background:white;border:1px solid #eeeaf7;padding:14px;border-radius:14px;}
div[data-testid="stTabs"] button {font-weight:700;}
</style>
<div class="hero">
  <div class="pill">YOUR FRIENDLY COLOR STUDIO</div>
  <h1>🎨 ColorPop<br>Find it. Match it. Make it colorful.</h1>
  <p>Choose a color, explore matching shades, or pick a color directly from an image.</p>
</div>
""", unsafe_allow_html=True)

def hex_to_rgb(hex_code):
    code = hex_code.lstrip("#")
    return tuple(int(code[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*[max(0, min(255, int(round(v)))) for v in rgb])

def color_name(hex_code):
    r, g, b = hex_to_rgb(hex_code)
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    if v < .12: return "Black"
    if s < .12: return "White" if v > .92 else "Gray"
    hue = h * 360
    if hue < 15 or hue >= 345: return "Red"
    if hue < 42: return "Orange"
    if hue < 68: return "Yellow"
    if hue < 155: return "Green"
    if hue < 190: return "Teal"
    if hue < 250: return "Blue"
    if hue < 285: return "Violet"
    if hue < 330: return "Pink"
    return "Magenta"

def hsl_hex(h, s, l):
    # colorsys uses HSV, so use a small HSL-to-RGB conversion
    h = (h % 360) / 360
    def hue_to_rgb(p, q, t):
        if t < 0: t += 1
        if t > 1: t -= 1
        if t < 1/6: return p + (q-p)*6*t
        if t < 1/2: return q
        if t < 2/3: return p + (q-p)*(2/3-t)*6
        return p
    if s == 0:
        r = g = b = l
    else:
        q = l*(1+s) if l < .5 else l+s-l*s
        p = 2*l-q
        r = hue_to_rgb(p,q,h+1/3)
        g = hue_to_rgb(p,q,h)
        b = hue_to_rgb(p,q,h-1/3)
    return rgb_to_hex((r*255,g*255,b*255))

def palette_for(hex_code):
    r,g,b = hex_to_rgb(hex_code)
    h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255)
    # Convert HSV value to a reasonable lightness approximation for harmonious shades.
    lightness = max(.25, min(.72, v*.62))
    sat = max(.4, min(.85, s))
    hues = [h*360, h*360+180, h*360+30, h*360+150, h*360+75]
    lights = [lightness, .62, .68, .52, .78]
    return [hex_code.upper()] + [hsl_hex(hue, sat, light) for hue,light in zip(hues[1:],lights[1:])]

def show_swatch(hex_code, label=None):
    name = color_name(hex_code)
    st.markdown(
        f"""<div style="background:{hex_code};height:100px;border-radius:15px;
        display:flex;align-items:flex-end;padding:10px;color:{'#fff' if sum(hex_to_rgb(hex_code))<390 else '#282342'};
        box-shadow:0 6px 16px #29204412;font-weight:800;">
        <span style="background:#ffffffd9;color:#282342;border-radius:8px;padding:5px 8px;font-size:12px;">{hex_code.upper()}</span>
        </div><div style="text-align:center;color:#77718c;font-size:12px;margin:5px 0 12px;">{label or name}</div>""",
        unsafe_allow_html=True
    )

left, right = st.columns([1, 1], gap="large")
with left:
    st.subheader("🖍️ Choose a color")
    chosen = st.color_picker("Pick your main color", "#7257FF")
    code = st.text_input("Or enter a HEX code", value=chosen.upper(), help="Example: #7257FF")
    code = code.strip()
    if not code.startswith("#"):
        code = "#" + code
    valid = len(code) == 7
    try:
        rgb = hex_to_rgb(code)
        valid = valid and all(0 <= channel <= 255 for channel in rgb)
    except (ValueError, TypeError):
        valid = False

    if valid:
        code = code.upper()
        r, g, b = hex_to_rgb(code)
        st.markdown(
            f'<div style="height:150px;background:{code};border-radius:18px;padding:18px;color:'
            f'{"white" if sum((r,g,b)) < 390 else "#282342"};display:flex;flex-direction:column;'
            f'justify-content:space-between;"><b>YOUR CURRENT COLOR</b><span style="font-size:25px;'
            f'font-weight:800;">{code} · {color_name(code)}</span></div>',
            unsafe_allow_html=True
        )
        m1, m2, m3 = st.columns(3)
        m1.metric("RED", r)
        m2.metric("GREEN", g)
        m3.metric("BLUE", b)
        st.code(f"HEX: {code}\nRGB: rgb({r}, {g}, {b})", language="text")
        if st.button("📋 Copy color code", use_container_width=True):
            st.info("Select the HEX value above and copy it. Clipboard access depends on your browser.")
    else:
        st.warning("Please enter a valid HEX code, such as #7257FF.")

with right:
    st.subheader("🌈 Matching palette")
    st.caption("A set of coordinated colors based on your selected shade.")
    if valid:
        swatches = palette_for(code)
        cols = st.columns(5)
        for col, shade in zip(cols, swatches):
            with col:
                show_swatch(shade)
        st.caption("Tip: tap a shade in the palette by entering its HEX code in the color field to explore it.")
    else:
        st.info("Enter a valid HEX code to see matching colors.")

st.divider()
st.subheader("🖼️ Identify a color from an image")
st.write("Upload a photo, then click a point on the image to sample its color.")
uploaded = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg", "webp"])
if uploaded:
    try:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, caption="Your image — click the image to sample a color", use_container_width=True)
        width, height = image.size
        x_col, y_col = st.columns(2)
        with x_col:
            x = st.number_input("Horizontal position (X)", min_value=0, max_value=max(0,width-1), value=width//2, step=1)
        with y_col:
            y = st.number_input("Vertical position (Y)", min_value=0, max_value=max(0,height-1), value=height//2, step=1)
        picked = rgb_to_hex(image.getpixel((int(x), int(y))))
        pr, pg, pb = hex_to_rgb(picked)
        st.markdown(
            f'<div style="background:{picked};padding:18px;border-radius:16px;color:'
            f'{"white" if sum((pr,pg,pb)) < 390 else "#282342"};font-size:22px;font-weight:800;">'
            f'{picked} — {color_name(picked)}</div>', unsafe_allow_html=True
        )
        st.write(f"RGB: ({pr}, {pg}, {pb})")
        st.caption("Coordinates start at the image's top-left corner. Use the X and Y fields to sample different points.")
    except Exception:
        st.error("This image could not be opened. Please try another image.")

st.divider()
st.caption("ColorPop • A simple color matching and identification project")
