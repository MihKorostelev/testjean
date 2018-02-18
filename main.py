import threading
import connect
import helllo
import change_my_answer
import status
import build
import server_watch
import create_remind
import delete_remind

rechange_request = threading.Thread(target=change_my_answer.infine_rechange_request)
rechange_request.start()
connect = threading.Thread(target=connect.infine_connect)
connect.start()
hello_command = threading.Thread(target=helllo.infine_hello)
hello_command.start()
status = threading.Thread(target=status.infine_status)
status.start()
build = threading.Thread(target=build.infine_build)
build.start()
watch_server = threading.Thread(target=server_watch.infine_monitor_server)
watch_server.start()
create_remind = threading.Thread(target=create_remind.infine_create_remind)
create_remind.start()
delete_remind = threading.Thread(target=delete_remind.infine_delete_remind)
delete_remind.start()
