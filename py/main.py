import encodings
from pickle import TRUE
from algosdk.v2client import *
from algosdk.encoding import *
#from algosdk.atomic_transaction_composer import AtomicTransactionComposer
from algosdk.atomic_transaction_composer import *
from algosdk.dryrun_results import *
from algosdk.future import transaction
from algosdk.abi.method import *
from util import *



def main():
    config = get_config()
    client = get_client(config)
    accts = get_accounts(config)

    addr, pk = accts[0]

    # Setup
    approval, clear = get_programs(client, config)
    app_id, app_addr = create_app(
        client,
        addr,
        pk,
        approval,
        clear,
        transaction.StateSchema(1, 0),
        transaction.StateSchema(0, 0),
    )

    # Create group txn
    sp = client.suggested_params()
    # contruct the ATC (Which supports ABI)
    atc = AtomicTransactionComposer()   
    # Create signer object
    signer = AccountTransactionSigner(pk)
    # Construct the method object
    meth1 = Method("add", [Argument("uint64")], Returns("uint64"))
    meth2 = Method("sub", [Argument("uint64")], Returns("uint64"))
    # Add a method call to the smart contract 
    atc.add_method_call(app_id, meth1, addr, sp, signer, method_args=[3])
    atc.add_method_call(app_id, meth2, addr, sp, signer, method_args=[1])

    # Execute the transaction
    result = atc.execute(client, 3);
    for result in result.abi_results:
        print("ABI Return Value: ",result.return_value)
    
    ################################################################
    #### -  All of the following code is for debugging    
    # execute a dryrun
    drr = transaction.create_dryrun(client, atc.gather_signatures())
    dr = client.dryrun(drr)

    dryrun_result = DryrunResponse(dr)

    for txn in dryrun_result.txns:
        if txn.app_call_rejected():
            print(txn.app_trace(StackPrinterConfig(max_value_width=30, top_of_stack_first=True)))
            print("Global Changes: ", txn.local_deltas)
            print("Local Changes: ",txn.global_delta)
            print("Opcode Cost: ",txn.cost)
            print("Logs: ",txn.logs)
            print("App Message: ",txn.app_call_messages)

    filename = "./dryrun.msgp"
    with open(filename, "wb") as f:
        import base64
        f.write(base64.b64decode(msgpack_encode(drr)))
#######################end of debugging code#############################
if __name__ == "__main__":
    main()
