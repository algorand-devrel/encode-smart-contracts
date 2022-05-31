from pyteal import *
from pyteal.ast import return_
 
"""Basic Counter Application"""
#specifically for ABI, future enhancements will improve this
return_prefix = Bytes("base16", "0x151f7c75")  # Literally hash('return')[:4]

@Subroutine(TealType.uint64)
def add(x):   
   return Seq(
        App.globalPut(Bytes("Count"), App.globalGet(Bytes("Count")) + x),
        Log(Concat(return_prefix, Itob(App.globalGet(Bytes("Count"))))),
        Approve()
   )

@Subroutine(TealType.uint64)
def deduct(x):    
    return Seq(
        If(App.globalGet(Bytes("Count")) >= x,
            App.globalPut(Bytes("Count"), App.globalGet(Bytes("Count")) - x),
        ),
        Log(Concat(return_prefix, Itob(App.globalGet(Bytes("Count"))))),
        Approve()
   )


def approval_program():
    
    handle_creation = Seq(
        App.globalPut(Bytes("Count"), Int(0)),
        Approve()
    )
    
    # new router coming that will simplify this
    handle_noop = Cond(
       [Txn.application_args[0] == MethodSignature("add(uint64)uint64"), Return(add(Btoi(Txn.application_args[1])))],
       [Txn.application_args[0] == MethodSignature("sub(uint64)uint64"), Return(deduct(Btoi(Txn.application_args[1])))],
    )
 
    # new router coming that will simplify this
    return Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.OptIn, Reject()],
        [Txn.on_completion() == OnComplete.CloseOut, Approve()],
        [Txn.on_completion() == OnComplete.UpdateApplication, Approve()],
        [Txn.on_completion() == OnComplete.DeleteApplication, Approve()],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )

 
def clear_state_program():
   return Approve()

def get_approval():
    return compileTeal(approval_program(), mode=Mode.Application, version=6)

def get_clear():
    return compileTeal(clear_state_program(), mode=Mode.Application, version=6)

if __name__ == "__main__":
    
    with open("app.teal", "w") as f:
        f.write(get_approval())

    with open("clear.teal", "w") as f:
        f.write(get_clear())

