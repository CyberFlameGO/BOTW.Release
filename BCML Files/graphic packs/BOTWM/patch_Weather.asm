[BotW_Weather_V208]
moduleMatches = 0x6267BFD0

.origin = codecave

weatherBytesMap:
.byte 0
.byte 1
.byte 2
.byte 3
.byte 4
.byte 5
.byte 6
.byte 7
.byte 8

_changeWeatherCalled:
b HookWeather
_changeWeather:
lis r6, weatherBytesMap@ha			; Load first part of the weather map's address
addi r6, r6, weatherBytesMap@l		; Load second part of the address
mulli r26, r26, 0x04				; .byte values are 4 byte aligned, so multiply the offset by 0x04
lbzx r26, r6, r26					; Load the byte that's stored in the weather map using it's address plus an offset which is the original weather value to "map" each one
stb r26, 0x18(r30)					; Original instruction that would store the weather
blr									; Return back to the link register

0x03668FCC = nop					; Replace instruction that checks whether the weather has changed. Since the value is always modified/changed, just disable this branch.
0x03668FEC = bla _changeWeatherCalled	; Replace instruction that normally stores the weather with a jump to the weather changing function

HookWeather:
addi r1, r1, -0x24
stw r3, 0(r1)
stw r4, 4(r1)
stw r5, 8(r1)
stw r6, 12(r1)
stw r7, 16(r1)
stw r8, 20(r1)
stw r9, 24(r1)
stw r10, 28(r1)
mflr r3
stw r3, 32(r1)


lis r3, weatherBytesMap@ha
addi r3, r3, weatherBytesMap@l
bla import.coreinit.WeatherSync


lwz r3, 32(r1)
mtlr r3
lwz r3, 0(r1)
lwz r4, 4(r1)
lwz r5, 8(r1)
lwz r6, 12(r1)
lwz r7, 16(r1)
lwz r8, 20(r1)
lwz r9, 24(r1)
lwz r10, 28(r1)
addi r1, r1, 0x24

b _changeWeather