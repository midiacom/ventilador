import enum
from typing import Any, Dict, Optional

import click
from miio import DeviceStatus, MiotDevice
from miio.click_common import EnumType, command, format_output

class OperationMode(enum.Enum):
    Normal = "normal"
    Nature = "nature"

class MoveDirection(enum.Enum):
    Left = "left"
    Right = "right"

MODEL_FAN_P9 = "dmaker.fan.p9"
MODEL_FAN_P10 = "dmaker.fan.p10"
MODEL_FAN_1C = "dmaker.fan.1c" # Este é o nosso

MIOT_MAPPING = {
    MODEL_FAN_P9: {
        # Definição das propriedades MIOT para o modelo P9
        # ...
    },
    MODEL_FAN_P10: {
        # Definição das propriedades MIOT para o modelo P10
        # ...
    },
    MODEL_FAN_1C: {
        "power": {"siid": 2, "piid": 1}, # Liga/Desliga
        "fan_speed": {"siid": 2, "piid": 2}, # Controle de Velocidade
        # Adicione outras propriedades conforme a documentação MIOT
    },
}

# Definição das classes FanStatusMiot e FanStatus1C
class FanMiot(MiotDevice):
    _mappings = MIOT_MAPPING

    @command(
        click.argument("speed", type=int),
        default_output=format_output("Setting speed to {speed}")
    )
    def set_speed(self, speed: int):
        # Defina a velocidade do ventilador
        if speed not in (1, 2, 3):
            raise ValueError("Invalid speed: %s" % speed)

        return self.set_property("fan_speed", speed)

    @command(
        click.argument("power", type=int),
        default_output=format_output("Fan power is {power}")
    )
    def set_power(self, power: int):
        # Defina o status do ventilador (on/off)
        if power not in (0, 1):
            raise ValueError("Invalid power value: %s" % power)

        return self.set_property("power", power)

# Função para interagir com o usuário e controlar o ventilador
def control_fan(ventilador):
    while True:
        print("Digite 0 para desligar o ventilador ou 1 para ligar:")
        try:
            power = int(input())
            if power == 0:
                ventilador.set_power(0)
                print("Ventilador desligado.")
            elif power == 1:
                print("Digite a velocidade desejada (1, 2 ou 3):")
                speed = int(input())
                if speed in (1, 2, 3):
                    ventilador.set_power(1)
                    ventilador.set_speed(speed)
                    print(f"Ventilador ligado com velocidade {speed}")
                else:
                    print("Velocidade inválida. Digite 1, 2 ou 3.")
            else:
                print("Opção inválida. Digite 0 para desligar ou 1 para ligar.")
        except ValueError:
            print("Entrada inválida. Digite 0 ou 1.")

if __name__ == "__main__":
    # Crie uma instância do ventilador
    ventilador = FanMiot("192.168.0.X", "abcefgh12345678")

    try:
        control_fan(ventilador)
    except KeyboardInterrupt:
        print("Script encerrado pelo usuário.")
