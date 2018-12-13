from django.shortcuts import render
import os,json
from mail_system_tool import settings
import extract_msg
import shutil
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import logging
from .helpers import common

logger = logging.getLogger('sourceDns.webdns.views')
directory = common.suffixDate()
formate_date = common.formateDate()

def index(request):
    # logger.error(directory)
    path = os.path.join(settings.BASE_DIR, 'mail_app', 'pending', directory)
    if os.path.exists(path + '/.DS_Store'):
        os.remove(path + '/.DS_Store')
    files = os.listdir(path)
    fileInfos = []
    for file in files:
        message = extract_msg.Message(os.path.join(path, file))
        fileInfo = {}
        fileInfo['filename'] = file
        subject = message.subject
        fileInfo['subject'] = subject
        fileInfos.append(fileInfo)
    return render(request, 'index.html', {'files': fileInfos, 'suffix_date': formate_date})

# if __name__ == '__main__':
#     index()

@csrf_exempt
def handleResult(request):
    if request.method == 'POST':
        path = os.path.join(settings.BASE_DIR, 'mail_app', 'pending', directory)
        complete_path = os.path.join(settings.BASE_DIR, 'mail_app', 'complete', directory)
        nojuanhao = os.path.join(complete_path, 'no')
        fileinfos = json.loads(bytes.decode(request.body))
        if not os.path.exists(nojuanhao):
            os.makedirs(nojuanhao)
        for file in fileinfos:
            logger.error(file.get('filename'))
            filename = file.get('filename')
            subject = file.get('file')
            suffix = file.get('suffix')
            if subject == '':
                shutil.copyfile(os.path.join(path, filename), os.path.join(nojuanhao, filename))
            else:
                first_split = subject.split(';')
                if len(first_split) == 1:
                    second_split = subject.split('-')
                    if len(second_split) == 1:
                        copy_file(os.path.join(path, filename), os.path.join(complete_path, second_split[0] + suffix))
                    else:
                        end = second_split[1].split('.')[0]
                        start = second_split[0][-len(end):]
                        for i in range(int(start), int(end) + 1):
                            if len(second_split[1].split('.', 1)) == 1:
                                copy_file(os.path.join(path, filename), os.path.join(complete_path, second_split[0][:-len(end)]) + str(i) + suffix)
                            else:
                                copy_file(os.path.join(path, filename), os.path.join(complete_path, second_split[0][:-len(end)]) + str(i) + '.' + second_split[1].split('.', 1)[1] + suffix)
                else:
                    for f in first_split:
                        # copy_file(os.path.join(path, filename),
                        #                 os.path.join(complete_path, f + suffix))
                        second_split = f.split('-')
                        if len(second_split) == 1:
                            copy_file(os.path.join(path, filename), os.path.join(complete_path, second_split[0] + suffix))
                        else:
                            end = second_split[1].split('.')[0]
                            start = second_split[0][-len(end):]
                            for i in range(int(start), int(end) + 1):
                                if len(second_split[1].split('.', 1)) == 1:
                                    copy_file(os.path.join(path, filename),
                                              os.path.join(complete_path, second_split[0][:-len(end)]) + str(i) + suffix)
                                else:
                                    copy_file(os.path.join(path, filename),
                                              os.path.join(complete_path, second_split[0][:-len(end)]) + str(i) + '.' +
                                              second_split[1].split('.', 1)[1] + suffix)
        return HttpResponseRedirect("/mail")

def copy_file(src, dst, count=0, ext='.msg'):
    if count == 0:
        destnation = dst + ext
    else:
        destnation = dst + str(count) + ext
    if os.path.exists(destnation):
        print(count)
        copy_file(src, dst, count + 1)
    else:
        shutil.copyfile(src, destnation)