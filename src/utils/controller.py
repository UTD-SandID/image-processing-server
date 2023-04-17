from rmbg_contour import getRescaleFactor

def process_image(sender, instance, created, **kwargs):
    coin_diameter = getattr(instance, 'coin_diameter')
    image_path = getattr(instance, 'image')
    var = getRescaleFactor(image_path, coin_diameter)
    if var == 0:
        setattr(instance, 'status', 'ready')
    else:
        setattr(instance, 'status', var)

