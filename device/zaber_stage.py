import zaber
  
class Zaber() :
    def __init__(self, logger=None ) :
        """  Initialize dome properties and capabilities
        """
        self.maxswitch = 1
        self.description = 'Zaber stage'
        self.name = 'Zaber focuser stage'
        self.minswitchvalue = 0
        self.maxswitchvalue = 50
        self.connect()

    def connect(self) :
        print('connect Zaber stage')
        self.zaber_stage=zaber.ZaberStage()
        self.connected = True

    def connected(self,state) :
        print('connected',state)
        return state

    def canwrite(self) :
        return True

    def disconnect(self) :
        self.connected(False)

    def get_description(self) :
        return self.description

    def get_name(self) :
        return self.name

    def set_position(self,val) :
        print('setting value',val)
        self.zaber_stage.move(float(val))

    def getswitch(self) :
        return True

    def get_value(self) :
        return self.zaber_stage.get_position()

    def get_step(self) :
         return 1

