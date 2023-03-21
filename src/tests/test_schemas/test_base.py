


from schemas.base import BaseArgs

def test_base_schema(base_schema_payload):
    payload, BaseArgs = base_schema_payload
    base_args = BaseArgs(**payload)
      
    assert base_args.dry_run == payload.get("--dry-run")
    assert base_args.non_interactive == payload.get("--non-interactive")
    assert base_args.help == payload.get("--help")
    assert base_args.user == payload.get("--user")
    assert base_args.verbose == payload.get("--verbose")
   