from collections import namedtuple
from matplotlib import colors

_max_rgb = 255.


def colors2_cmap_and_norm(name, colors_dict):
    cmap_dict = _rawdict2cmapdict(colors_dict)
    norm = colors.Normalize(min(colors_dict), max(colors_dict), clip=False)
    return colors.LinearSegmentedColormap(name, cmap_dict), norm


def _rawdict2cmapdict(colors_dict):
    cmap_dict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }
    maxbndy = max(colors_dict)
    minbndy = min(colors_dict)

    if maxbndy == minbndy:
        raise ValueError("Color map requires more than one color")

    for bndy in colors_dict:
        clrs = colors_dict[bndy]
        lvl = (bndy - minbndy) / (maxbndy - minbndy)
        hasalpha = hasattr(clrs[0], 'a')
        alphas = [clr.a if hasalpha else 1.0 for clr in clrs]
        relclrs = [rgba(clr.r / _max_rgb, clr.g / _max_rgb, clr.b / _max_rgb, alpha) for clr, alpha in
                   zip(clrs, alphas)]
        if len(relclrs) == 1:
            relclrs *= 2
        cmap_dict['red'].append((lvl, relclrs[0].r, relclrs[1].r))
        cmap_dict['green'].append((lvl, relclrs[0].g, relclrs[1].g))
        cmap_dict['blue'].append((lvl, relclrs[0].b, relclrs[1].b))
        cmap_dict['alpha'].append((lvl, relclrs[0].a, relclrs[1].a))

    return cmap_dict


#################################################
#    Converting .pal to dictionary of colors    #
#################################################


def from_pal(palfile):
    colorbar = {}
    with open(palfile) as paldata:
        for line in paldata:
            bndy, clrs = _parse_pal_line(line)
            if bndy is not None:
                colorbar[int(bndy)] = clrs
    return colorbar


def _parse_pal_line(line):
    tokens = line.split()
    header = tokens[0] if tokens else None

    if header is not None and 'color' in header.lower():
        cdata = tokens[1:]
        isrgba = 'color4' in header.lower()
        if not cdata:
            return None, None
        bndy = cdata[0]
        rgba_vals = cdata[1:]
        clrs = [_getcolor(rgba_vals, isrgba)]

        if len(rgba_vals) > 4:
            index = 4 if isrgba else 3
            rgba_vals = rgba_vals[index:]
            clrs.append(_getcolor(rgba_vals, isrgba))

        return bndy, tuple(clrs)

    return None, None


def _getcolor(rgba_vals, has_alpha):
    if has_alpha:
        alpha = float(rgba_vals[3]) / _max_rgb
        return rgba(r=int(rgba_vals[0]), g=int(rgba_vals[1]), b=int(rgba_vals[2]), a=alpha)
    else:
        return rgb(r=int(rgba_vals[0]), g=int(rgba_vals[1]), b=int(rgba_vals[2]))


rgb = namedtuple('rgb', 'r g b')
rgba = namedtuple('rgba', 'r g b a')
