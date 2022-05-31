from pyteal import *

args = Txn.application_args

abi_match = lambda selector: args[0] == selector

on_complete = lambda oc: Txn.on_completion() == oc

isCreate = Txn.application_id() == Int(0)
isOptIn = on_complete(OnComplete.OptIn)
isClear = on_complete(OnComplete.ClearState)
isClose = on_complete(OnComplete.CloseOut)
isUpdate = on_complete(OnComplete.UpdateApplication)
isDelete = on_complete(OnComplete.DeleteApplication)
isNoOp = on_complete(OnComplete.NoOp)


return_prefix = Bytes("base16", "0x151f7c75")  # Literally hash('return')[:4]

@Subroutine(TealType.uint64)
def raise_to_power(x, y):
    i = ScratchVar(TealType.uint64)
    a = ScratchVar(TealType.uint64)

    return Seq(
        a.store(x),
        For(i.store(Int(1)), i.load() <= y, i.store(i.load() + Int(1))).Do(
                a.store(a.load()*x),
        ),
        Log(Concat(return_prefix, Itob(a.load()))),
        a.load(),
    )


def approval():

    router = Cond(
        [args[0] == MethodSignature("raise(uint64,uint64)uint64"), raise_to_power(Btoi(args[1]), Btoi(args[2])-Int(1))],
    )

    return Cond(
        [isCreate, Approve()],
        [isOptIn, Approve()],
        [isClear, Approve()],
        [isClose, Approve()],
        [isUpdate, Approve()],
        [isDelete, Approve()],
        [isNoOp, Return(router)]
    )
    
def clear():
    return Approve()

def get_approval():
    return compileTeal(approval(), mode=Mode.Application, version=6)


def get_clear():
    return compileTeal(clear(), mode=Mode.Application, version=6)


if __name__ == "__main__":
    with open("app.teal", "w") as f:
        f.write(get_approval())

    with open("clear.teal", "w") as f:
        f.write(get_clear())
