from biblishelf_core.command import BaseCommand



class Test(BaseCommand):
    description = "test3"
    help = "test1"



class Lv2(Test):
    description = "test4"
    help = """
    aaa
    """