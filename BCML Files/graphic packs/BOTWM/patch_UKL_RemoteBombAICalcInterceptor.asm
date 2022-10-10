[BotW_UKL_RemoteBombAIInterceptor_V208]
moduleMatches = 0x6267BFD0

.origin = codecave

UKL_RemoteBombAIInterceptor_ModuleName:
.string "ukl_remotebombaiinterceptor" ; Unfortunately it doesn't seem like this can be capitalized

UKL_RemoteBombAIInterceptor_ModuleHandle:
.int 0

UKL_RemoteBombAIInterceptor_ForceExplode_Name:
.string "ForceExplode"

UKL_RemoteBombAIInterceptor_ForceExplode_Loc:
.int 0


OnAICalc:
; Backup LR
addi r1, r1, -8
stw r3, 4(r1)
mflr r3
stw r3, 0(r1)
lwz r3, 4(r1)
; Backup the rest of the registers
bl UKL_Utils_CreateRegStore
addi r1, r1, -4
stw r3, 0(r1) ; RegStore* will be in stack

addi r1, r1, -0x4
li r3, 0x0 ; Default value in case function cannot be called.
stw r3, 0x0(r1) ; Function should return value to stack here.

lis r3, UKL_RemoteBombAIInterceptor_ForceExplode_Name@ha
addi r3, r3, UKL_RemoteBombAIInterceptor_ForceExplode_Name@l
lis r4, UKL_RemoteBombAIInterceptor_ModuleName@ha
addi r4, r4, UKL_RemoteBombAIInterceptor_ModuleName@l
lis r5, UKL_RemoteBombAIInterceptor_ForceExplode_Loc@ha
addi r5, r5, UKL_RemoteBombAIInterceptor_ForceExplode_Loc@l
lis r6, UKL_RemoteBombAIInterceptor_ModuleHandle@ha
addi r6, r6, UKL_RemoteBombAIInterceptor_ModuleHandle@l
lwz r7, 4(r1)
bl UKL_Utils_DynamicBranch

lbz r3, 0x0(r1)
addi r1, r1, 0x4
cmpwi r3, 0x1 ; expect return in r8, since DynamicBranch uses the others
bne OnAICalc_Exit
stb r3, 0x78(r29) ; Just set the explode flag to true. Lazy so we use r3.

OnAICalc_Exit:
; Restore the rest of the registers
lwz r3, 0(r1)
addi r1, r1, 4
bl UKL_Utils_LoadRegStore
bl UKL_Utils_DisposeRegStore
; Restore LR
stw r3, 4(r1)
lwz r3, 0(r1)
mtlr r3
lwz r3, 4(r1)
addi r1, r1, 8

; Execute original instruction
lbz r11, 0x78(r29)

; Return to execution
b 0x02872388

; Slightly before remote bomb AI decides if the bomb should explode.
0x02872384 = b OnAICalc
