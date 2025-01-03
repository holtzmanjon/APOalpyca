import lts
  
class LTS150() :
    def __init__(self, logger=None ) :
        """  Initialize dome properties and capabilities
        """
        self.maxswitch = 1
        self.description = 'Thorlabs LTS 150'
        self.name = 'Iodine stage'
        self.minswitchvalue = 0
        self.maxswitchvalue = 1500
        self.connect()

    def connect(self) :
        print('connect LTS 150')
        self.lts_stage=lts.ThorlabsStage()
        self.connected = True

    def connected(self,state) :
        print('connected',state)
        return state

    def canwrite(self,id) :
        return True

    def disconnect(self) :
        self.connected(False)

    def get_description(self,id) :
        return self.description

    def get_name(self,id) :
        return self.name

    def get_minvalue(self,id) :
        return self.minswitchvalue

    def get_maxvalue(self,id) :
        return self.maxswitchvalue

    def set_value(self,id,val) :
        print('setting value',val)
        self.lts_stage.move(float(val))

    def getswitch(self,id) :
        return True

    def get_value(self,id) :
        return self.lts_stage.get_position()

    def get_step(self,id) :
         return 1

