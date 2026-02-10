# WCAG2ICT

## 1.Perceivable

### 1.1 Text Alternatives

#### 1.1.1 Non-text Content
* For this requirement to be met, alternative text should be added to the to the non-text elements
* This alternative text should be readable by screen readers
* I plan to use maps, graphs and icons in my application. In this case I need to add alternative text to them.
* Especially with maps and graphs alternative text should priotize information. While icons priotize functionality.
* Maps should have markers added as focusable UI elements. When user focuses on markers, screen reader should read the alternative text.

### 1.2 Time-based Media

* In this project I don't plan to use videos, audio recordings or other types of time-based media.

### 1.3 Adaptable

#### 1.3.1 Info and Relationships

* You need to label the UI component so it could be read by the screen readers

#### 1.3.2 Meaningful Sequence

* Content should be on a programatically determined sequence which is meaningful.
* I should consider the experience of a user navigating my app with a keyboard. This user's order of reading UI elements should be meaningful.

#### 1.3.3 Sensory Characteristics

* "Instructions provided for understanding and operating content do not rely solely on sensory characteristics of components such as shape, color, size, visual location, orientation, or sound."
* This means user should be able to execute the commands application gives to the user without understanding:
    * Shape of a certain object
    * Color of a certain object
    * Without needing to locate the object by looking at the screen
    * Without needing to hear a certain sound effect

#### 1.3.4 Orientation(AA)
* My app should support different display sizes and orientations.
* The content on my app should be resistant to resizing.

### 1.4 Distinguishable

#### 1.4.1 Use of Color
* Color shouldn't be used as the only way of conveying information. There should be alternative ways.

#### 1.4.3 Contrast(Minimum)(AA)
* Any text should have contrast color compared to the background.
* For normal text contrast should be at least 4.5:1
* For lage text contrast should be at least 3:1

## 2.Operable

### 2.1 Keyboard Accessible

#### 2.1.1 Keyboard
* Content should be operable and navigatable with keyboard-only.
* Keyboard should be able to do anything that mouse can do.
* Keyboard actions shouldn't require individual keystrokes for navigation.

#### 2.1.2 No Keyboard Trap
* Keyboard-only users shouldn't be trapped.
* There must be an keyboard-only exit method at all times.

### 2.2 Enough Time

* This section is not relevant because, I don't plan to time-based content. User will always have enough time to read and use the content.

### 2.3 Seizures and Physical Reactions

#### 2.3.1 Seizures and Physical Reactions

* It should be under 3 flashes in 1 second.
* I plan to use no flashes.

### 2.4 Navigable

#### 2.4.1 Bypass Blocks
* I should add a key to bypass blocks of content.
* Most common key for this task is 'tab'.

#### 2.4.2 Page Titled

* This requirement demands every screen and window is titled properly and according to the function of it.

#### 2.4.3 Focus Order

* Elements should recieve focus in an order that preserves meaning.
* When users navigate a website with keyboard only, order of elements for them should make sense.

#### 2.4.4 Link Purpose (In Context)

* Non-web software doesn't have links exactly. Instead this requirement should be applied to control components such as buttons.
* "Links" should make it clear where they are taking the user to.
* The text and alt-text should define the next location "link" takes the user to.

#### 2.4.6 Headings and Labels(AA)

* Headings and labels should describe the content related to them properly.

#### 2.4.7 Focus Visible

* Focused element should have a visual effect to distinguish it from non-focused elements.

### 2.5 Input Modalities

#### 2.5.1 Pointer Gestures

* This requirement is not relevant because I don't plan to use gestures.

#### 2.5.2 Pointer Cancellation

* This requirement concerns all my buttons.
* My buttons should not execute with a down-event. They should execute with an up-event.
* Button should give visual feedback after the down-event but shouldn't start executing the functionality.
* If user moves the click away from the button between down and up events, the execution of button function should cancel.

#### 2.5.3 Label in Name

* Internal name for a button and the text of the button should match.
* People who operate with voice interaction may use the visible text to refer the element.
* If a user who operates with voice interaction refers an element with visible text and internal name is diffrent this can result in command not executing as intended to.

#### 2.5.4 Motion Actuation

* This requirement is not relevant because my application will not use device motion.

#### 2.5.8 Target Size (Minimum)

* Buttons should be at least 24x24 pixels.
* It should be easy to click the buttons.

## 3. Understandable

### 3.1 Readable

#### 3.1.1 Language of Page

* The screen reader should detect the language of the page.
* Implementation of this highly depends on the platform.

### 3.2 Predictable

#### 3.2.1 On Focus

* When a UI element recieves focus, it shouldn't initiate a change of context.
* Change of context means changing viewport, focus or content in a major way.

#### 3.2.2 On Input

* Changing the value or setting of any UI component shouldn't automatically cause change of context.
* Users should be warned.
* On input changes shouldn't be unexpected.

#### 3.2.3 Consistent Navigation(AA)

* Mechanisms and shortcuts used for navigation should be consistent.

#### 3.2.6 Consistent Help

* If my application will have a help mechanism, it should be presented in the same order all the time.
* Order is: Human contact details, Human contact mechanism, Self-help option and a fully automated contact mechanism.
* In this point of development I am not sure if application will have all these help mechanisms.
* It is important that requirement says "if". Which means it is optional to add these help mechanisms.

### 3.3 Input Assistance

#### 3.3.1 Error Identification

* If an input error is automatically detected, the item that is in error is identified and the error is described to the user in text.
* Error feedback message should be understandable by non-technical people.

#### 3.3.2 Labels or Instructions

* Labels or instructions are provided when content requires user input.
* This clarifies what input is asked from the user.
* Instructions should be clear and not vague.

#### 3.3.7 Redundant Entry

* Previously entered information should be either auto-populated or available user to select within a finite amount of options.
* Exceptions are when re-entering the information is essential or when previously entered information is no longer valid.

## 4. Robust

### 4.1 Compatible

#### 4.1.1 Parsing (WCAG 2.1)

* This requirement doesn't apply to my app.
* This requirement only applies to software authored with a markup language.

#### 4.1.2 Name, Role, Value

* Incomplete











