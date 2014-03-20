def uninstall(portal):
    setup_tool = portal.portal_setup
    setup_tool.runAllImportStepsFromProfile(
        'profile-uniofleicester.jscontent:uninstall')
    return "Imported uninstall profile."
