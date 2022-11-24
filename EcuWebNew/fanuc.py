#coding=utf-8
import eel
from ctypes import *
from flask import Flask, jsonify, render_template
from forms import LoginForm, FortyTwoForm, NewPostForm, UploadForm,  SigninForm, \
    RegisterForm, SigninForm2, RegisterForm2, CmdForm, WIFIForm, LANForm, AddForm,FortyThreeForm

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# @app.route('/')
# def wyl():
#     #lib = cdll.LoadLibrary("libfcdq.so")
#     #b = lib.ReadProgNum3()
#     b = [3]
#     return render_template('main.html', a = b)

@app.route('/inqure')
def inqure():
    #lib = cdll.LoadLibrary("libfcdq.so")
    #b = lib.ReadProgNum3()
    b = [3]
    return render_template('inqure.html', a = b)

@app.route('/test')
def test():
    #lib = cdll.LoadLibrary("libfcdq.so")
    #b = lib.ReadProgNum3()
    return render_template('fanucwyll.html')

@app.route("/", methods=["GET", "POST"])
def ioctl():
    wifiform = WIFIForm()
    lanform  = LANForm()

    usb_info_list=[]
    usb_info = os.popen("ifconfig").read()
    usb_info_list = usb_info.splitlines(False)

    if wifiform.validate_on_submit():
        if wifiform.publish.data  and wifiform.validate():
            ssid = wifiform.ssid.data
            pwd = wifiform.pwd.data
            ip =  wifiform.static_ip.data

            cmd0 = 'ifconfig wlan0 down'
            cmd1 = 'head -n 4 /etc/wpa_supplicant.conf > /etc/wpa_supplicant.conf.tmp'
            cmd2 = 'wpa_passphrase '+ ssid + ' ' + pwd + '>> /etc/wpa_supplicant.conf.tmp'
            cmd3 = 'mv /etc/wpa_supplicant.conf /etc/wpa_supplicant.conf.bak'
            cmd4 = 'mv /etc/wpa_supplicant.conf.tmp /etc/wpa_supplicant.conf'
            cmd5 = 'ifconfig wlan0 up'
            cmd6 = 'udhcpc -i wlan0 &'
            cmd7 = 'ifconfig wlan0 '+ip
            cmd8 = 'wpa_supplicant -D nl80211 -c /etc/wpa_supplicant.conf -i wlan0 -B'
            cmd9 = 'killall -9 udhcpc'
            sig = ' && '
            sig1 = ' && '
            print(ip)
            flash('ip %s'%ip)
            cmd_intgrate = cmd0+sig+cmd1+sig+cmd2+sig+cmd3+sig+cmd4+sig+cmd8+sig+cmd5
            get_cmd_timeout(cmd_intgrate)
            if ip == '' :
                 dhcp_cmd = cmd9 + sig + cmd6
                 ret = get_cmd_timeout(dhcp_cmd)
                 #flash('The command < %s > execute results list at the page bottom!!!'%dhcp_cmd)
            else:
                ret = get_cmd_timeout(cmd7)
                #flash('The command < %s > execute results list at the page bottom!!!'%cmd7)
            print(ret)

    if lanform.validate_on_submit():
        if lanform.publish.data  and lanform.validate():
            gateway = lanform.gateway.data
            mask = lanform.mask.data
            ip =  lanform.static_ip.data

            getbr0 = get_cmd_timeout('ifconfig br0')
            if getbr0.find('Device not found'.encode()                  ) != -1:
                cmd1 = 'cd /usr/winston/'
                cmd2 = './bridge.sh'
                cmd_f = cmd1 + ' && ' + cmd2
                get_cmd_timeout(cmd_f)

            ifcmd = 'ifconfig br0 '
            if ip != '':
                ifcmd = ifcmd + ip
            if mask != '':
                ifcmd = ifcmd + ' netmask ' + mask
            ifcmdresult = get_cmd_timeout(ifcmd)
            print(ifcmd)

            if gateway != '':
                gwcmd = 'route add default gw '+gateway
                gwfeedbk = get_cmd_timeout(gwcmd)
                print(gwcmd)
                #flash('The command < %s > executed!!!'%gwcmd)

    return render_template('iofeedback.html', wifiform=wifiform, lanform=lanform, usb_info_list=usb_info_list)

#eel.init('templates')

@eel.expose
def my_add(a, b):
    print(123)
    return a+b

#eel.start('main.html',mode='edge')

if __name__ =='__main__':
    app.run(debug=True,host="127.0.0.1",port=5000)
