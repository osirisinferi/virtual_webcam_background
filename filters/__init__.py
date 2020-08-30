filters = {}


def register_filter(name, filter):
    global filters
    filters[name] = filter


def get_filter(name):
    return filters.get(name, None)


def get_filters(config, filter_list):
    image_filters = []
    for filters_item in filter_list:
        if type(filters_item) == str:
            filter_class = get_filter(filters_item)
            image_filters.append(filter_class())
        if type(filters_item) == list:
            filter_name = filters_item[0]

            params = filters_item[1:]
            _args = []
            _kwargs = {}
            if len(params) == 1 and type(params[0]) == list:
                # ["filtername", ["value1", "value2"]]
                _args = params[0]
            elif len(params) == 1 and type(params[0]) == dict:
                # ["filtername", {param1: "value1", "param2": "value2"}]
                _kwargs = params[0]
            else:
                # ["filtername", "value1", "value2"]
                _args = params

            image_filter_class = get_filter(filter_name)
            if not image_filter_class:
                continue

            image_filters.append(image_filter_class(config=config,
                                                    *_args, **_kwargs))
    return image_filters


def apply_filters(frame, mask, part_masks, heatmap_masks, image_filters):
    for image_filter in image_filters:
        frame = image_filter.apply(frame=frame, mask=mask,
                                   part_masks=part_masks,
                                   heatmap_masks=heatmap_masks)
    return frame


from . import grayscale
from . import blur
from . import gaussian_blur
from . import color
from . import roll
from . import transparency
from . import noise
from . import transformations
from . import stripes
from . import images
from . import video
from . import webcam
from . import anonymize
from . import hologram
