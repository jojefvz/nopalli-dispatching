class Dispatcher():
    @classmethod
    def update_broker(name, street_address, city, state, zipcode):
        pass

    @classmethod
    def preassign_driver(driver, dispatch):
        dispatch.driver_ref = driver.reference
        driver.preassigned_dispatches.append(dispatch.reference)

    @classmethod
    def propose_dispatch(driver, dispatch):
        proposal = dispatch.generate_proposal()

        driver.receive_proposal(proposal)

    @classmethod
    def receive_driver_answer(dispatch, driver):
        answer = driver.generate_answer()

        dispatch.receive_answer(answer)


