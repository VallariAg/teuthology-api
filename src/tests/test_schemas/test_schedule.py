
def test_schedule_schema(base_schema_payload, schedule_schema_payload):
    """
    test ScheduleArgs schema which inherits from BaseArgs
    use the base_schema fixtures
    """
    bs_payload, _ = base_schema_payload

    ss_payload, SchedulerArgs = schedule_schema_payload

    ss_payload.update(bs_payload)

    schedule_args = SchedulerArgs(**ss_payload)
      
    assert schedule_args.dry_run == ss_payload.get("--dry-run")
    assert schedule_args.non_interactive == ss_payload.get("--non-interactive")
    assert schedule_args.help == ss_payload.get("--help")
    assert schedule_args.user == ss_payload.get("--user")
    assert schedule_args.filter_all == None
    assert schedule_args.subset == None
    assert schedule_args.owner == ss_payload.get("--owner")
    assert schedule_args.force_priority == ss_payload.get("--force-priority")
    assert schedule_args.no_nested_subset == ss_payload.get("--no-nested-subset")
    assert schedule_args.job_threshold == ss_payload.get("--job-threshold")
   




