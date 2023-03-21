
def test_kill_schema(base_schema_payload, kill_schema_payload):
    """
    test ScheduleArgs schema which inherits from BaseArgs
    use the base_schema fixtures
    """
    bs_payload, _ = base_schema_payload
    ks_payload, KilArgs = kill_schema_payload

    ks_payload.update(bs_payload)

    kill_args = KilArgs(**ks_payload)
      
    assert kill_args.owner == ks_payload.get("--owner")
    assert kill_args.run == ks_payload.get("--run")
    assert kill_args.preserve_queue == ks_payload.get("--preserve-queue")
    assert kill_args.job == ks_payload.get("--job")
    assert kill_args.machine_type == ks_payload.get("--machine-type")
    assert kill_args.archive == ks_payload.get("--archive")
   
   
    