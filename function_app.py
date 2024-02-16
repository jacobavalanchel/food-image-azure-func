import azure.functions as func
import logging
import shutil
from ultralytics import YOLO
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient,BlobClient,ContainerClient
import os,uuid

def uploadToCt(data):
    connection_string = "DefaultEndpointsProtocol=https;AccountName=imageclassds;AccountKey=ZfuhniUPWj/SsV/Nqod2lb80fvV0rg+NFl4NLOrz9TnjYLFfOEwhF/2qOOYBgEdhAyjk74ykNtLx+AStklYlPQ==;EndpointSuffix=core.windows.net"
    app = func.FunctionApp()
    try:
        pic_dir="./runs/detect/predict/Five_tips_Stream.jpg"
        with open(pic_dir, "rb") as file:
            binary_data = file.read()
        logging.info("try conneting to ct")
        print("trial-logging")

        # Quickstart code goes here
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container="food-image-task", blob="result.jpg")
        blob_client.upload_blob(binary_data,overwrite=True)
        print("done uploading")
        shutil.rmtree("./runs")
        print("cleared")
        logging.info("done uploading")
    except Exception as ex:
        logging.info('Exception:')
        logging.info(ex)




@app.blob_trigger(arg_name="myblob", path="imageclassds",
                               connection="imageclassds_STORAGE") 
def FoodRecogBlobTrigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
    # 模型路径
    model = YOLO("best.pt")

    # 预测图片路径，输出结果保存
    result = model(source='Five_tips_Stream.jpg', save=True)