import ee
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context
# ee.Authenticate()
ee.Initialize(project='ee-juliaszymanska142')


def create_cloud_free_mosaic(aoi, start_date, end_date):
    s2 = ee.ImageCollection('COPERNICUS/S2') \
        .filterBounds(aoi) \
        .filterDate(start_date, end_date)

    def cloud_mask(image):
        qa = image.select('QA60')
        cloud_bit = 1 << 10
        cirrus_bit = 1 << 11
        mask = qa.bitwiseAnd(cloud_bit).eq(0).And(
            qa.bitwiseAnd(cirrus_bit).eq(0))
        return image.updateMask(mask).copyProperties(image, image.propertyNames())

    masked_collection = s2.map(cloud_mask)

    mosaic = masked_collection.median().clip(aoi)

    return mosaic
