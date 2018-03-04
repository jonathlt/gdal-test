from osgeo import ogr, osr
ogr.UseExceptions()

database = 'test'
usr = 'postgres'
pw = 'mysecretpassword'
host = '192.168.1.82'
table = 'example'

inDataSource = ogr.Open("example_wrapper.vrt")
inLayer = inDataSource.GetLayer('example')

connectionString = "PG:dbname='%s' user='%s' password='%s' host='%s'" % (database,usr,pw,host)
ogrds = ogr.Open(connectionString)

srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

outLayer = ogrds.CreateLayer(table, srs, ogr.wkbPoint, ['OVERWRITE=YES','LAUNDER=NO'] )

# Add input Layer Fields to the output Layer if it is the one we want
inLayerDefn = inLayer.GetLayerDefn()
for i in range(0, inLayerDefn.GetFieldCount()):
    fieldDefn = inLayerDefn.GetFieldDefn(i)
    print(inLayerDefn.GetFieldDefn(i).GetNameRef())
    #print(fieldDefn)
    #fieldName = fieldDefn.GetName()
    #print(fieldName)
    outLayer.CreateField(fieldDefn)

outLayerDefn = outLayer.GetLayerDefn()

for feat in inLayer:

    new_feature = ogr.Feature(outLayerDefn)

    # Add field values from input Layer
    for i in range(0, outLayerDefn.GetFieldCount()):
        fieldDefn = outLayerDefn.GetFieldDefn(i)
        #fieldName = fieldDefn.GetName()
        #print(fieldName)
        #print(outLayerDefn.GetFieldDefn(i).GetNameRef())
        new_feature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(),
            feat.GetField(i))

    geom = feat.GetGeometryRef()
    new_feature.SetGeometry(geom.Clone())
    print(geom.ExportToWkt())
    outLayer.StartTransaction()
    outLayer.CreateFeature(new_feature)
    new_feature = None
    outLayer.CommitTransaction()
