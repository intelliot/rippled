# Notary Escrow Pseudo-code

In this example, the exported `main` function is called during an `EscrowFinish` transaction.

The function only allows the escrow to finish if the finish transaction's account matches the allowed notary account.

```
pub fn main() -> bool {
    // Retrieve finish transaction details from the host environment.
    let finish_tx = unsafe { host_lib::get_tx() };

    // Define the notary account allowed to release the escrow.
    // TODO: Retrieve this value from the escrow object's data?
    let allowed_account = "rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh";

    // Check if the finish transaction's account matches the allowed account.
    if finish_tx.account == allowed_account {
        return true;
    }
    false
}

pub mod host_lib {
    extern "C" {
        pub fn get_tx() -> Tx;
    }
}

// Pseudo-structure representing transaction details.
pub struct Tx {
    pub account: &'static str,
}
```
