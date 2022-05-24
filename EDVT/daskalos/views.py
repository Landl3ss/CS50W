# from cProfile import run
from django.shortcuts import render

# Create your views here.

def index(request):

    if request.method == "POST":
        run_type = request.POST.getlist('run_type')

        try:
            b = request.POST['bootuut']
        except:
            b = 'no'
        
        try:
            m = request.POST['marginpower']
        except:
            m = 'no'

        try:
            p = request.POST['powercycle']
        except:
            p = 'no'

        try:
            t = request.POST['temp_enabled']
        except:
            t = 'no'
        
        bootuut = b
        marginpower = m
        powercycle = p
        temp_enabled = t

        with open('daskalos/static/files/cfg.txt', 'w') as cfg:
            cfg.write(
                '# Config file for EDVT script\n\n'
                '[version]\n'
                'cfg_version = 1.02'
                '\n\n'
                '[uut]\n'
                '#BLD 14 EDVT\n'
                f"uutIP = {request.POST['uut_ip']}\n"
                f"uutPort = {request.POST['uut_port']}\n"
                "\n"
                '[apc]\n'
                f"apcIP = {request.POST['apc_ip']}\n"
                f"apcPort1 = {request.POST['apc_port1']}\n"
                f"apcPort2 = {request.POST['apc_port2']}\n"
                f"apcPwd = {request.POST['apc_password']}\n"
                "\n"
                "[chamber]\n"
                f"chamberIP = {request.POST['chamber_ip']}\n"
                f"chamberPort = {request.POST['chamber_port']}\n"
                f"chamberType = {request.POST['chamber_type']}\n"
                "\n"
                "[ixia]\n"
                f"ixiaIP1 = {request.POST['ixia_ip1']}\n"
                f"ixiaIP2 = {request.POST['ixia_ip2']}\n"
                f"ixiaCardType = {request.POST['ixia_card_type']}\n"
                f"ixiaCard1 = {request.POST['ixia_card_1']}\n"
                f"ixiaCard2 = {request.POST['ixia_card_2']}\n"
                f"ixiaCard3 = {request.POST['ixia_card_3']}\n"
                f"ixiaCard4 = {request.POST['ixia_card_4']}\n"
                f"ixiaPort1 = {request.POST['ixia_port_1']}\n"
                f"ixiaPort2 = {request.POST['ixia_port_2']}\n"
                f"ixiaPort3 = {request.POST['ixia_port_3']}\n"
                f"ixiaPort4 = {request.POST['ixia_port_4']}\n"
                f"ixiaUser = {request.POST['ixuser']}\n"
                f"ixiaVersion = {request.POST['ixversion']}\n"
                "\n"
                "[edvt]\n"
                f"run_type = {run_type[0]}\n"
                f"corner_1 = {request.POST['corner1']}\n"
                f"corner_2 = {request.POST['corner2']}\n"
                f"corner_3 = {request.POST['corner3']}\n"
                f"corner_4 = {request.POST['corner4']}\n"
                f"high_temp = {request.POST['hitemp']}\n"
                f"low_temp = {request.POST['lotemp']}\n"
                f"nom_temp = {request.POST['nomtemp']}\n"
                f"loopPerCorner = {request.POST['loop_per_corner']}\n"
                f"timePerCorner = {request.POST['time_per_corner']}\n"
                f"stopOnFailure = {request.POST['stop_on_failure']}\n"
                f"tempEnable = {temp_enabled}\n"
                f"powerCycle = {powercycle}\n"
                f"marginPwr = {marginpower}\n"
                f"bootuut = {bootuut}\n"
                "\n"
                f"powerOffWaitTime = {request.POST['pwr_off_wait_time']}\n"
                f"powerOffSoakTime = {request.POST['pwr_off_soak_time']}\n"
                f"powerOnWaitTime = {request.POST['pwr_on_wait_time']}\n"
                f"powerOnSoakTime = {request.POST['pwr_on_soak_time']}\n"
                "\n"
                "[pwrsupply]\n"
                f"pwrNumMarg = {request.POST['pwr_num_marg']}\n"
                f"pwr0 = {request.POST['pwr0']}\n"
                f"pwr0_hi = {request.POST['pwr0_hi']}\n"
                f"pwr0_lo = {request.POST['pwr0_lo']}\n"
                f"pwr1 = {request.POST['pwr1']}\n"
                f"pwr1_hi = {request.POST['pwr1_hi']}\n"
                f"pwr1_lo = {request.POST['pwr1_lo']}\n"
                f"pwr2 = {request.POST['pwr2']}\n"
                f"pwr2_hi = {request.POST['pwr2_hi']}\n"
                f"pwr2_lo = {request.POST['pwr2_lo']}\n"
                f"pwr3 = {request.POST['pwr3']}\n"
                f"pwr3_hi = {request.POST['pwr3_hi']}\n"
                f"pwr3_lo = {request.POST['pwr3_lo']}\n"
                f"pwr4 = {request.POST['pwr4']}\n"
                f"pwr4_hi = {request.POST['pwr4_hi']}\n"
                f"pwr4_lo = {request.POST['pwr4_lo']}\n"
                f"pwr5 = {request.POST['pwr5']}\n"
                f"pwr5_hi = {request.POST['pwr5_hi']}\n"
                f"pwr5_lo = {request.POST['pwr5_lo']}\n"
                f"pwr6 = {request.POST['pwr6']}\n"
                f"pwr6_hi = {request.POST['pwr6_hi']}\n"
                f"pwr6_lo = {request.POST['pwr6_lo']}\n"
                f"pwr7 = {request.POST['pwr7']}\n"
                f"pwr7_hi = {request.POST['pwr7_hi']}\n"
                f"pwr7_lo = {request.POST['pwr7_lo']}\n"
                "\n"
                "[prompts]\n"
                f"bios_pmpt = {request.POST['bios_pmpt']}\n"
                f"diag_pmpt = {request.POST['diag_pmpt']}\n"
                f"dsh_pmpt = {request.POST['dsh_pmpt']}\n"
                "\n"
                f"ios_pmpt = {request.POST['ios_pmpt']}\n"
                f"ios_dp_pmpt = {request.POST['ios_dp_pmpt']}\n"
                f"ios_cfg_pmpt = {request.POST['ios_cfg_pmpt']}\n"
                f"ios_cfgif_pmpt = {request.POST['ios_cfgif_pmpt']}\n"
                f"ios_brcm_pmpt = {request.POST['ios_brcm_pmpt']}\n"
                "\n"
                "[ios]\n"
                f"ios_login = {request.POST['ios_login']}\n"
                f"ios_pswd = {request.POST['ios_passwd']}\n"
                f"ios_traffic_time = {request.POST['ios_traffic']}\n"
                f"ios_sleep_interval = {request.POST['ios_sleep_interval']}\n"
                f"ixia_cfg_file = {request.POST['ixia_cfg_file']}\n"
                f"ixia_start_cfg_file = {request.POST['ixia_start_cfg_file']}\n"
                f"ixia_stop_cfg_file = {request.POST['ixia_stop_cfg_file']}\n"
                f"ixia_dump_cnt_cfg_file {request.POST['ixia_dmp_cfg_file']}\n"
                "\n"
                "[image]\n"
                f"diag_image = {request.POST['diag_image']}\n"
                f"ios_image = {request.POST['ios_image']}\n"
                "\n"
                "[user_defined]\n"
                f"user_diag_test = {request.POST['usr_diag_test']}\n"
                f"user_ios_test = {request.POST['usr_ios_test']}")



    return render(request, 'daskalos/index.html')