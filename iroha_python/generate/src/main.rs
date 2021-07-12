//! Binary which generates classes from json schema

use std::collections::BTreeMap;
use std::env;

use iroha_schema::prelude::*;
use module::Module;

mod as_py;
mod module;

macro_rules! to_json {
    ($($t:ty),* $(,)?) => {{
        let mut out = BTreeMap::new();
        $(<$t as IntoSchema>::schema(&mut out);)*
		out
    }};
}

fn get_metamap() -> MetaMap {
    use iroha_data_model::prelude::*;
    use iroha_data_model::query::QueryBox;

    to_json!(Value, Instruction, Expression, QueryBox, EventFilter,)
}

fn main() -> Result<(), iroha_error::Reporter> {
    iroha_error::install_panic_reporter();

    let args = &env::args().collect::<Vec<_>>()[1..];
    if args.is_empty() {
        Err(iroha_error::error!(
            "Please provide argument with valid directory"
        ))?
    }

    let module = get_metamap().into_iter().collect::<Module>();
    module.write_dir(&args[0])?;
    Ok(())
}
