# The Flow of the Redux design pattern is:
1. An action is being invoked (with/without a payload.
1. If there is a relevant Effect that written to this certain action:
- The effect catch the action and call service or use its own functionality. 
- Finally the effect dispatch a new action/ new actions.

3. If there is a relevant reducer written to this certain action:
- The reducer changes the state in the store.
4. The components listens to changes in store using selectors and react accordingly (change certain things in ui/ call actions etc...)

# The following schema shows the flow graphically:
![Redux flow example.jpg](/.attachments/Redux%20flow%20example-83b0a841-d65f-433c-a473-0cf4b481ec2a.jpg)