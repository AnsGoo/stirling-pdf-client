from ast import List
from ctypes import Array
from pathlib import Path
from typing import Optional, Any,Literal
from httpx import Client, Response
import re
import urllib


class ConvertApi:

    __client: Client
    def __init__(self, client:Client) -> None:
        self.__client = client

    def url_to_pdf(self, urlInput:str) -> str:
        url = '/api/v1/convert/url/pdf'
        resp:Response = self.__client.request(method='POST', url=url, data={"urlInput":urlInput})

        return resp.text
    
    def pdf_to_xml(self, file_input:Path, fileId:str) -> Any:
        url = '/api/v1/convert/pdf/xml'
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        with open(file_input, 'rb') as file:
            files = {"fileInput": file}
            data = {
                'fileId': fileId
            }

            resp:Response = self.__client.request(method='POST', url=url, data=data, files=files)
            return resp.json()
        
    
    def pdf_to_word(self,  out_path:Path, file_input:Optional[Path], fileId:Optional[str]= None, output_format: Optional[str]='doc') -> str:
        # 确保output_format只能是'doc'或'docx'
        
        if output_format not in ['doc', 'docx']:
            raise ValueError("output_format must be either 'doc' or 'docx'")

        if file_input is None  and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        url = '/api/v1/convert/pdf/word'
        file = None
        if file_input:
            file = open(file_input, 'rb')
        files = {"fileInput": file}
        data = {
            'fileId': fileId,
            "outputFormat": output_format
        }
        resp:Response = self.__client.request(method='POST', url=url, data=data, files=files)
        self._save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.status_code


    def pdf_to_text(self, out_path:Path, file_input:Optional[Path],fileId:Optional[str]= None, output_format: Optional[str]='rtf') -> str:
        url = '/api/v1/convert/pdf/text'
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        if file_input is None  and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, 'rb')
        files = {"fileInput": file}
        data = {
            'fileId': fileId,
            "outputFormat": output_format
        }
        resp:Response = self.__client.request(method='POST', url=url, data=data, files=files)
        self._save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.status_code

    def pdf_to_presentation(self, out_path:Path, file_input:Optional[Path],fileId:Optional[str]= None, output_format: Optional[str]='ppt') -> str:
        url = '/api/v1/convert/pdf/presentation'
        if output_format not in ['ppt', 'pptx']:
            raise ValueError("output_format must be either 'ppt' or 'pptx'")
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        if file_input is None  and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, 'rb')
        files = {"fileInput": file}
        data = {
            'fileId': fileId,
            "outputFormat": output_format
        }
        resp:Response = self.__client.request(method='POST', url=url, data=data, files=files)
        self._save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.status_code

    def pdf_to_pdfa(self, out_path:Path, file_input:Optional[Path],fileId:Optional[str]= None, output_format: Optional[str]='pdfa') -> str:
        url = '/api/v1/convert/pdf/pdfa'
        if output_format not in ['pdfa', 'pdfa-1']:
            raise ValueError("output_format must be either 'pdfa' or 'pdfa-1'")
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        if file_input is None  and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, 'rb')
        files = {"fileInput": file}
        data = {
            'fileId': fileId,
            "outputFormat": output_format
        }
        resp:Response = self.__client.request(method='POST', url=url, data=data, files=files)
        self._save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.status_code

    def pdf_to_markdown(self, out_path:Path, file_input:Optional[Path],fileId:Optional[str]= None) -> str:
        url = '/api/v1/convert/pdf/markdown'
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        if file_input is None  and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, 'rb')
        files = {"fileInput": file}
        data = {
            'fileId': fileId
        }
        resp:Response = self.__client.request(method='POST', url=url, data=data, files=files)
        self._save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.status_code

    def pdf_to_img(self, out_path:Path, file_input:Optional[Path],fileId:Optional[str]= None,page_numbers:str='all',image_format:Literal['png','jpg','jpeg','gif','webp']='png',single_or_multiple:Literal['single','multiple']='multiple',color_type:Literal['color','greyscale','blackwhite']='color',dpi:int=300,include_annotations:Optional[bool]=False) -> str:
        url = '/api/v1/convert/pdf/img'
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        if file_input is None  and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, 'rb')
        files = {"fileInput": file}
        data = {
            'fileId': fileId,
            "pageNumbers":page_numbers,
            "imageFormat":image_format,
            "singleOrMultiple":single_or_multiple,
            "colorType":color_type,
            "dpi":dpi,
            "includeAnnotations":include_annotations
        }
        resp:Response = self.__client.request(method='POST', url=url, data=data, files=files)
        self._save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.status_code

    def pdf_to_html(self, out_path:Path, file_input:Optional[Path],fileId:Optional[str]= None) -> str:
        url = '/api/v1/convert/pdf/html'
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        if file_input is None  and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, 'rb')
        files = {"fileInput": file}
        data = {
            'fileId': fileId
        }
        resp:Response = self.__client.request(method='POST', url=url, data=data, files=files)
        self._save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.status_code

    def pdf_to_csv(self, out_path:Path, file_input:Optional[Path],fileId:Optional[str]= None, page_numbers:str='all') -> str:
        url = '/api/v1/convert/pdf/html'
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        if file_input is None  and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, 'rb')
        files = {"fileInput": file}
        data = {
            'fileId': fileId,
            "pageNumber":page_numbers
        }
        resp:Response = self.__client.request(method='POST', url=url, data=data, files=files)
        self._save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.status_code

    def markdown_to_pdf(self, out_path:Path, file_input:Path) -> str:
        url = '/api/v1/convert/pdf/html'
        
        file = open(file_input, 'rb')
        files = {"fileInput": file}
        resp:Response = self.__client.request(method='POST', url=url, files=files)
        self._save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.status_code

    def img_to_pdf(self, out_path:Path, file_input:List[Path],fit_option:Literal['fillPage','fitDocumentToImage','maintainAspectRatio']='fillPage',color_type:Literal['color','greyscale','blackwhite']='color',auto_rotate:Optional[bool]=False) -> str:
        url = '/api/v1/convert/pdf/html'
        
        file_list = map(file_input,lambda file: open(file, 'rb'))
        files = {"fileInput": file_list}
        data = {
            "fitOption":fit_option,
            "colorType":color_type,
            "autoRotate":auto_rotate
        }
        resp:Response = self.__client.request(method='POST', url=url, files=files, data=data)
        self._save_file(resp=resp, out_path=out_path)
        for file in file_list:
            file.close()
        return resp.status_code

    def html_to_pdf(self, out_path:Path, file_input:Optional[Path] = None, fileId:Optional[str]= None, zoom:Optional[float]=1.0) -> str:
        url = '/api/v1/convert/pdf/html'
        if file_input is None  and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        
        file = open(file_input, 'rb')
        files = {"fileInput": file}
        data = {
            "zoom":zoom,
            "fileId":fileId
        }
        resp:Response = self.__client.request(method='POST', url=url, files=files, data=data)
        self._save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.status_code

    def file_to_pdf(self, out_path:Path, file_input:Path) -> str:
        url = '/api/v1/convert/pdf/html'
        file = open(file_input, 'rb')
        files = {"fileInput": file}

        resp:Response = self.__client.request(method='POST', url=url, files=files)
        self._save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.status_code

    def eml_to_pdf(self, out_path:Path, file_input:Optional[Path] = None,fileId:Optional[str]= None, include_attachments:Optional[bool]=False, max_attachment_size_mb:Optional[int]=10, download_html:Optional[bool] = False,include_all_recipients:Optional[bool]=True ) -> str:
        url = '/api/v1/convert/pdf/html'
        if file_input is None  and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, 'rb')
        files = {"fileInput": file}
        data = {
            "includeAttachments":include_attachments,
            "maxAttachmentSizeMB":max_attachment_size_mb,
            "downloadHtml":download_html,
            "includeAllRecipients":include_all_recipients
        }

        resp:Response = self.__client.request(method='POST', url=url, files=files, data=data)
        self._save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.status_code

    def _save_file(self, resp:Response, out_path:Path):
        target_file = out_path
        if not out_path.is_file():
            filename = self._get_filename(resp)
            target_file = out_path.joinpath(filename)
        with open(target_file, 'wb') as f:
            f.write(resp.content)

    def _get_filename(self, resp:Response, default_filename="unkown_filename")-> str:
        """提取文件名的主方法"""
        headers = resp.headers
        content_disposition = headers.get('content-disposition', '')
        
        # 从Content-Disposition提取
        if content_disposition:
            match = re.search(r'filename\*?=([^;]+)', content_disposition, re.IGNORECASE)
            if match:
                filename = match.group(1).strip(' "\'')
                # 处理编码
                if filename.startswith("UTF-8''") or filename.startswith("utf-8''"):
                    filename = urllib.parse.unquote(filename[7:])
                return re.sub(r'[<>:"/\\|?*]', '_', filename)
        return default_filename

    