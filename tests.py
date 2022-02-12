import re
from sty import fg, bg, rs # for colors in print
from sendmypie.main import update_add_more, enter_email

class TestSendMyPie:
    def setup(self):
        print("in setup")
        return

    def test_enter_email(self):
        print("\033[2J")
        print(f"\n\n{bg.black} Run TESTS for function {fg.yellow}enter_email() {fg.rs} {fg.li_blue}{self}{fg.rs} {bg.rs}\n\n")

        print(f"input addr = {bg.black} {fg.li_red}'fdskjfdj'{fg.rs} => {fg.cyan}emails_addresses == []{fg.rs} {bg.rs}")
        # print(f"TEST {self} DATA input addr = 'fdskjfdj' => emails_addresses == []")
        emails_addresses = enter_email(addr="fdskjfdj", add_more=False)
        assert emails_addresses == []
        # print(f"assert {emails_addresses == []}\n")
        print(f"assert {bg.black} {fg.li_blue}{str(emails_addresses == [])}{fg.rs} {bg.rs}\n")


        print(f"input addr = {bg.black} {fg.li_red}'name space'{fg.rs} => {fg.cyan}emails_addresses == []{fg.rs} {bg.rs}")
        # print(f"TEST {self} DATA input addr = 'name space' => emails_addresses == []")
        emails_addresses = enter_email(addr="name space", add_more=False)
        assert emails_addresses == []
        # print(f"assert {emails_addresses == []}\n")
        print(f"assert {bg.black} {fg.li_blue}{str(emails_addresses == [])}{fg.rs} {bg.rs}\n")


        print(f"input addr = {bg.black} {fg.li_red}'name@'{fg.rs} => {fg.cyan}emails_addresses == []{fg.rs} {bg.rs}")
        # print(f"TEST {self} DATA input addr = 'name@' => emails_addresses == []")
        emails_addresses = enter_email(addr="name@", add_more=False)
        assert emails_addresses == []
        # print(f"assert {emails_addresses == []}\n")
        print(f"assert {bg.black} {fg.li_blue}{str(emails_addresses == [])}{fg.rs} {bg.rs}\n")


        print(f"input addr = {bg.black} {fg.li_red}'name@domain'{fg.rs} => {fg.cyan}emails_addresses == []{fg.rs} {bg.rs}")
        # print(f"TEST {self} DATA input addr = 'name@domain' => emails_addresses == []")
        emails_addresses = enter_email(addr="name@domain", add_more=False)
        assert emails_addresses == []
        # print(f"assert {emails_addresses == []}\n")
        print(f"assert {bg.black} {fg.li_blue}{str(emails_addresses == [])}{fg.rs} {bg.rs}\n")


        print(f"input addr = {bg.black} {fg.li_red}'name@domain.'{fg.rs} => {fg.cyan}emails_addresses == []{fg.rs} {bg.rs}")
        # print(f"TEST {self} DATA input addr = 'name@domain.' => emails_addresses == []
        emails_addresses = enter_email(addr="name@domain.", add_more=False)
        assert emails_addresses == []
        # print(f"assert {emails_addresses == []}\n")
        print(f"assert {bg.black} {fg.li_blue}{str(emails_addresses == [])}{fg.rs} {bg.rs}\n")


        print(f"input addr = {bg.black} {fg.li_red}'name@domain.y'{fg.rs} => {fg.cyan}emails_addresses == []{fg.rs} {bg.rs}")
        # print(f"TEST {self} DATA input addr = 'name@domain.y' => emails_addresses == []")
        emails_addresses = enter_email(addr="name@domain.y", add_more=False)
        assert emails_addresses == []
        # print(f"assert {emails_addresses == []}\n")
        print(f"assert {bg.black} {fg.li_blue}{str(emails_addresses == [])}{fg.rs} {bg.rs}\n")


        print(f"input addr = {bg.black} {fg.li_red}'name@domain.yyyy'{fg.rs} => {fg.cyan}emails_addresses == []{fg.rs} {bg.rs}")
        # print(f"TEST {self} DATA input addr = 'name@domain.yyyy' => emails_addresses == []")
        emails_addresses = enter_email(addr="name@domain.yyyy", add_more=False)
        assert emails_addresses == []
        # print(f"assert {emails_addresses == []}\n")
        print(f"assert {bg.black} {fg.li_blue}{str(emails_addresses == [])}{fg.rs} {bg.rs}\n")


        print(f"input addr = {bg.black} {fg.li_red}'name@domain.fr'{fg.rs} => {fg.cyan}emails_addresses[0] == 'name@domain.fr'{fg.rs} {bg.rs}")
        # print(f"TEST {self} DATA input addr = 'name@domain.fr' => emails_addresses[0] == 'name@domain.fr'")
        emails_addresses = enter_email(addr="name@domain.fr", add_more=False)
        assert emails_addresses[0] == "name@domain.fr"
        # print(f"assert {emails_addresses[0] == 'name@domain.fr'}\n")
        print(f"assert {bg.black} {fg.li_blue}{str(emails_addresses[0] == 'name@domain.fr')}{fg.rs} {bg.rs}\n")


        print(f"input addr = {bg.black} {fg.li_red}'nick.name@domain.it'{fg.rs} => {fg.cyan}emails_addresses[0] == 'nick.name@domain.it'{fg.rs} {bg.rs}")
        # print(f"TEST {self} DATA input addr = 'nick.name@domain.it' => emails_addresses[0] == 'nick.name@domain.it'")
        emails_addresses = enter_email(addr="nick.name@domain.it", add_more=False)
        assert emails_addresses[0] == 'nick.name@domain.it'
        # print(f"assert {emails_addresses[0] == 'nick.name@domain.it'}\n")
        print(f"assert {bg.black} {fg.li_blue}{str(emails_addresses[0] == 'nick.name@domain.it')}{fg.rs} {bg.rs}\n")


        print(f"input addr = {bg.black} {fg.li_red}'nick.name@domain.ext'{fg.rs} => {fg.cyan}emails_addresses[0] == 'nick.name@domain.ext'{fg.rs} {bg.rs}")
        # print(f"TEST {self} DATA input addr = 'nick.name@domain.ext' => emails_addresses[0] == 'nick.name@domain.ext'")
        emails_addresses = enter_email(addr="nick.name@domain.ext", add_more=False)
        assert emails_addresses[0] == 'nick.name@domain.ext'
        # print(f"assert {emails_addresses[0] == 'nick.name@domain.ext'}\n")
        print(f"assert {bg.black} {fg.li_blue}{str(emails_addresses[0] == 'nick.name@domain.ext')}{fg.rs} {bg.rs}\n")


        print(f"input addr = {bg.black} {fg.li_red}'small-buddy.comeny@soda-elsy.com'{fg.rs} => {fg.cyan}emails_addresses[0] == 'small-buddy.comeny@soda-elsy.com'{fg.rs} {bg.rs}")
        # print(f"TEST {self} DATA input addr = 'small-buddy.comeny@soda-elsy.com' => emails_addresses[0] == 'small-buddy.comeny@soda-elsy.com'")
        emails_addresses = enter_email(addr='small-buddy.comeny@soda-elsy.com', add_more=False)
        assert emails_addresses[0] == 'small-buddy.comeny@soda-elsy.com'
        # print(f"assert {emails_addresses[0] == 'small-buddy.comeny@soda-elsy.com'}\n")
        print(f"assert {bg.black} {fg.li_blue}{str(emails_addresses[0] == 'small-buddy.comeny@soda-elsy.com')}{fg.rs} {bg.rs}\n")


        print(f"input addr = {bg.black} {fg.li_red}['small-buddy.comeny@soda-elsy.com', 'small-buddy.comeny@soda-elsy.com', 'josy@campana.be']{fg.rs}")
        print(f"=> {fg.cyan}emails_addresses[0] == ['small-buddy.comeny@soda-elsy.com', 'small-buddy.comeny@soda-elsy.com', 'josy@campana.be']{fg.rs} {bg.rs}")
        # print(f"TEST {self} DATA input addr = input => emails_addresses[0] == input")
        emails_addresses = enter_email(addr=['small-buddy.comeny@soda-elsy.com', 'small-buddy.comeny@soda-elsy.com', 'josy@campana.be'], 
            add_more=False)
        assert emails_addresses == ['small-buddy.comeny@soda-elsy.com', 'small-buddy.comeny@soda-elsy.com', 'josy@campana.be']
        # print(f"assert {emails_addresses[0] == input}\n")
        print(f"assert {bg.black} {fg.li_blue}{str(emails_addresses == ['small-buddy.comeny@soda-elsy.com', 'small-buddy.comeny@soda-elsy.com', 'josy@campana.be'])}{fg.rs} {bg.rs}\n")


        return


if __name__ == '__main__':
    # test email format
    TestSendMyPie.test_enter_email(TestSendMyPie)