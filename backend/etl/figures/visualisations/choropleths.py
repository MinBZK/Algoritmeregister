import base64

def plotly_fig_to_png(fig):
    img_bytes = fig.to_image(format="png")
    base64_bytes = base64.b64encode(img_bytes)
    return base64_bytes.decode()

