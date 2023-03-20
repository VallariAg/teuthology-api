
def test_suite_schema(base_schema_payload, suite_schema_payload):
    """
    test ScheduleArgs schema which inherits from BaseArgs
    use the base_schema fixtures
    """
    bs_payload, _ = base_schema_payload
    ss_payload, SuiteArgs = suite_schema_payload

    ss_payload.update(bs_payload)

    suite_args = SuiteArgs(**ss_payload)
      
    assert suite_args.dry_run == ss_payload.get("--dry-run")
    assert suite_args.suite == ss_payload.get("--suite")
    assert suite_args.suite_branch == ss_payload.get("--suite-branch")
    assert suite_args.suite_repo == ss_payload.get("--suite-repo")
   
   

