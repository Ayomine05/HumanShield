"""
Scenario data and the adaptive-difficulty selection logic.
Kept separate from app.py so routing/API logic and scenario
content don't have to live in one giant file.
"""

SCENARIOS_BY_CATEGORY = {
    "finance": {
        "Beginner": "finance-otp-1",
        "Advanced": "finance-otp-2",
        "Expert": "finance-adaptive-1"
    },
    "work": {
        "Intermediate": "work-bec-1",
        "Advanced": "work-bec-2",
        "Expert": "work-adaptive-1"
    },
    "social": {
        "Intermediate": "social-verify-1",
        "Advanced": "social-verify-2",
        "Expert": "social-adaptive-1"
    },
    "personal": {
        "Beginner": "personal-romance-2",
        "Advanced": "personal-romance-1",
        "Expert": "personal-adaptive-1"
    },
    "education": {
        "Beginner": "education-scholarship-1",
        "Advanced": "education-scholarship-2",
        "Expert": "education-adaptive-1"
    },
    "economy": {
        "Beginner": "economy-grant-1",
        "Advanced": "economy-grant-2",
        "Expert": "economy-adaptive-1"
    },
    "shopping": {
        "Beginner": "shopping-delivery-1",
        "Advanced": "shopping-delivery-2",
        "Expert": "shopping-adaptive-1"
    },
    "government": {
        "Intermediate": "government-immigration-1",
        "Advanced": "government-immigration-2",
        "Expert": "government-adaptive-1"
    },
    "gaming": {
        "Beginner": "gaming-rewards-1",
        "Advanced": "gaming-rewards-2",
        "Expert": "gaming-adaptive-1"
    }
}

DIFFICULTY_ORDER = ["Beginner", "Intermediate", "Advanced", "Expert"]


def get_next_difficulty(last_score):
    if last_score is None:
        return "Beginner"
    if last_score >= 90:
        return "Expert"
    if last_score >= 75:
        return "Advanced"
    if last_score >= 50:
        return "Intermediate"
    return "Beginner"


def pick_scenario_for_category(category_id, last_score):
    available = SCENARIOS_BY_CATEGORY.get(category_id)
    if not available:
        return None, None

    target_difficulty = get_next_difficulty(last_score)
    if target_difficulty in available:
        return available[target_difficulty], target_difficulty

    for difficulty in DIFFICULTY_ORDER:
        if difficulty in available:
            return available[difficulty], difficulty

    return None, None


def get_scenarios():
    step1_choice_a_feedback = (
        "Risky. Shortened links hide the real destination, "
        "and urgency plus threat of suspension is a classic "
        "pressure tactic to stop you thinking it through."
    )
    step1_choice_b_feedback = (
        "Safer than clicking, but if it were real, ignoring it "
        "could actually matter. The strongest move is to verify "
        "independently."
    )
    step1_choice_c_feedback = (
        "Correct. Verifying through a channel you already trust, "
        "not one the message gave you, is the core defense "
        "against this attack."
    )
    step2_choice_a_feedback = (
        "Correct. Reporting helps your provider flag the number, "
        "and deleting removes the temptation to revisit it later."
    )
    step2_choice_b_feedback = (
        "Risky. Replying confirms your number is active and "
        "monitored, which can lead to more targeted attempts."
    )

    finance2_step1_a_feedback = (
        "Risky. Banks never ask you to read a code back to them "
        "\u2014 that code almost certainly authorizes the caller's "
        "own fraudulent transaction on your account, not a reversal "
        "of anything."
    )
    finance2_step1_b_feedback = (
        "Correct. Hanging up and calling the number on your card "
        "yourself removes the attacker from the conversation "
        "entirely, so nothing they say can pressure you further."
    )
    finance2_step1_c_feedback = (
        "Risky. Staying on the call while checking your app still "
        "keeps the attacker talking and pressuring you \u2014 and "
        "your app won't show a transaction that hasn't happened yet."
    )
    finance2_step2_a_feedback = (
        "Correct. Reporting the attempted fraud and changing your "
        "credentials closes off whatever access or information the "
        "caller may already have."
    )
    finance2_step2_b_feedback = (
        "Risky. Assuming it's over without changing anything leaves "
        "you exposed if the caller has other account details."
    )

    education_step1_a_feedback = (
        "Risky. Legitimate scholarships never require you to pay a "
        "fee to receive money \u2014 that pattern only runs in one "
        "direction with real awards."
    )
    education_step1_b_feedback = (
        "Correct. Checking for the organization independently, "
        "rather than trusting the email's own claims, is exactly "
        "how you catch a fake scholarship board."
    )
    education_step2_a_feedback = (
        "Correct. Reporting and not paying protects both you and "
        "anyone else who might receive the same email."
    )
    education_step2_b_feedback = (
        "Risky. \"It's a small amount\" is exactly the reasoning "
        "these scams count on \u2014 the fee is designed to feel "
        "low-risk enough to pay without checking further."
    )

    economy_step1_a_feedback = (
        "Risky. Your BVN is sensitive financial ID \u2014 no "
        "legitimate government scheme asks for it, or a fee, "
        "through an unsolicited WhatsApp message."
    )
    economy_step1_b_feedback = (
        "Correct. Real government empowerment schemes don't request "
        "personal ID numbers or payment through messages like this."
    )
    economy_step2_a_feedback = (
        "Correct. Blocking and warning others helps limit how far "
        "this specific scam spreads."
    )
    economy_step2_b_feedback = (
        "Risky. Asking for \"proof\" keeps you engaged with the "
        "scammer and signals you're a responsive target worth "
        "continuing to pursue."
    )

    work_step1_a_feedback = (
        "Risky. Acting immediately on an urgent, secretive money "
        "request \u2014 especially one asking you not to call \u2014 "
        "is exactly the pressure and isolation pattern BEC scams rely on."
    )
    work_step1_b_feedback = (
        "Risky. Replying through the same email thread doesn't help "
        "\u2014 if the account is compromised or spoofed, the attacker "
        "just answers your reply too."
    )
    work_step1_c_feedback = (
        "Correct. Confirming through a separate, already-trusted "
        "channel \u2014 not the one the request arrived on \u2014 is "
        "the only real way to verify identity here."
    )
    work_step2_a_feedback = (
        "Correct. Reporting lets your IT or security team block "
        "similar attempts and warn other staff."
    )
    work_step2_b_feedback = (
        "Risky. Not reporting it means colleagues could still fall "
        "for the same message."
    )

    social_step1_a_feedback = (
        "Risky. This mimics the platform's real login page closely, "
        "but entering your password on a link from a DM \u2014 not "
        "the app itself \u2014 hands your credentials straight to "
        "the attacker."
    )
    social_step1_b_feedback = (
        "Correct. Account threats sent as urgent DMs from unfamiliar "
        "accounts are a common takeover attempt. Checking your "
        "account status inside the real app avoids the trap entirely."
    )
    social_step2_a_feedback = (
        "Correct. Since your account shows no actual issue, the DM "
        "was fake \u2014 blocking and reporting helps the platform "
        "catch the account sending it."
    )
    social_step2_b_feedback = (
        "Risky. Replying keeps the conversation going and confirms "
        "your account is active and being watched by someone."
    )

    personal_step1_a_feedback = (
        "Risky. Urgent emergencies from someone you've never met in "
        "person, especially early in an online relationship, are a "
        "textbook romance scam pattern \u2014 the emotional urgency "
        "is designed to bypass your judgment."
    )
    personal_step1_b_feedback = (
        "Correct. Slowing down and questioning a request for money "
        "from someone you haven't verified in person is exactly the "
        "right instinct here."
    )
    personal_step2_a_feedback = (
        "Correct. A refusal to video call or meet, especially paired "
        "with more urgency, is a strong confirmation this isn't a "
        "genuine relationship."
    )
    personal_step2_b_feedback = (
        "Risky. Sending money after this response only confirms "
        "you're willing to pay despite the refusal to verify \u2014 "
        "expect further requests."
    )

    shopping_step1_a_feedback = (
        "Risky. Small, urgent fee requests to \"release\" a package "
        "are a common delivery scam pattern designed to feel too "
        "minor to question."
    )
    shopping_step1_b_feedback = (
        "Correct. Checking the tracking number directly through the "
        "courier's own official app or site bypasses the fake link "
        "entirely."
    )
    shopping_step2_a_feedback = (
        "Correct. Reporting and deleting it prevents you from "
        "second-guessing yourself into paying later."
    )
    shopping_step2_b_feedback = (
        "Risky. Once your tracking shows no issue, paying \"just in "
        "case\" only rewards the scam."
    )

    government_step1_a_feedback = (
        "Risky. Threat of arrest paired with a demand for immediate "
        "payment by transfer is a pressure tactic \u2014 real "
        "government agencies don't operate this way over a phone call."
    )
    government_step1_b_feedback = (
        "Correct. Verifying through the office's official contact "
        "details, not the number that called you, is the only way "
        "to confirm this is real."
    )
    government_step2_a_feedback = (
        "Correct. Reporting the call helps authorities track and "
        "warn against the specific impersonation attempt."
    )
    government_step2_b_feedback = (
        "Risky. Not reporting it means the same call likely goes "
        "on to target others."
    )

    gaming_step1_a_feedback = (
        "Risky. Legitimate game rewards are claimed inside the "
        "official app or site \u2014 never by entering your login "
        "on a separate, unfamiliar page."
    )
    gaming_step1_b_feedback = (
        "Correct. Real promotions don't need your password on a "
        "third-party site \u2014 ignoring the link avoids handing "
        "over your account entirely."
    )
    gaming_step2_a_feedback = (
        "Correct. Reporting it in-game helps flag the scam to the "
        "platform, and keeping your login private protects your "
        "account going forward."
    )
    gaming_step2_b_feedback = (
        "Risky. Game accounts often hold payment info and personal "
        "data too \u2014 \"just a game account\" undersells what's "
        "actually at risk."
    )

    work2_step1_a_feedback = (
        "Risky. A near-identical vendor domain with one extra "
        "character is a classic spoofing trick \u2014 updating "
        "payment details based on the email alone sends your "
        "money straight to the attacker."
    )
    work2_step1_b_feedback = (
        "Correct. Confirming through a phone number you already "
        "have on file \u2014 not one in the email \u2014 is the "
        "only reliable way to verify a bank detail change."
    )
    work2_step1_c_feedback = (
        "Risky. Asking the sender to confirm in writing still "
        "trusts the same compromised or spoofed channel \u2014 "
        "they'll happily \"confirm\" whatever they already sent."
    )
    work2_step2_a_feedback = (
        "Correct. Flagging the suspicious domain protects your "
        "team from being targeted by the same fraud later."
    )
    work2_step2_b_feedback = (
        "Risky. Not reporting it means colleagues in finance could "
        "still fall for the same fake domain."
    )

    social2_step1_a_feedback = (
        "Risky. This is the account-recovery-transfer trick: the "
        "code sent to you is likely for taking over your own "
        "account, not helping a friend recover theirs."
    )
    social2_step1_b_feedback = (
        "Correct. Confirming through a channel you already know "
        "belongs to your friend \u2014 not the account that "
        "messaged you \u2014 is the only way to catch an "
        "impersonation like this."
    )
    social2_step2_a_feedback = (
        "Correct. Warning shared contacts helps stop the "
        "compromised account from reaching more people."
    )
    social2_step2_b_feedback = (
        "Risky. Staying quiet leaves others in your shared circles "
        "exposed to the same message."
    )

    personal2_step1_a_feedback = (
        "Risky. A stranger declaring love and requesting money "
        "almost immediately is one of the most direct romance scam "
        "patterns \u2014 no real relationship moves this fast."
    )
    personal2_step1_b_feedback = (
        "Correct. Blocking and reporting immediately, without "
        "engaging further, is the right call when the pattern is "
        "this obvious."
    )
    personal2_step2_a_feedback = (
        "Correct. Confirming your decision and warning others "
        "helps people around you recognize the same pattern."
    )
    personal2_step2_b_feedback = (
        "Risky. Reconsidering out of guilt is exactly the emotional "
        "lever these scams are built to pull."
    )

    education2_step1_a_feedback = (
        "Risky. Real interview processes don't require a "
        "\"refundable deposit\" through an email link \u2014 that "
        "payment step is the actual goal of the scam."
    )
    education2_step1_b_feedback = (
        "Correct. Checking your application status by logging into "
        "the official portal yourself, not through the email's "
        "link, confirms whether any of this is real."
    )
    education2_step1_c_feedback = (
        "Risky. Calling a number the email itself provided still "
        "keeps you inside the attacker's setup \u2014 they'll just "
        "answer and confirm whatever they already told you."
    )
    education2_step2_a_feedback = (
        "Correct. Reporting it helps the university's security team "
        "warn other applicants targeted by the same email."
    )
    education2_step2_b_feedback = (
        "Risky. Assuming a missing requirement is just an oversight "
        "is exactly the benefit-of-the-doubt these scams rely on."
    )

    economy2_step1_a_feedback = (
        "Risky. Legitimate employers never require new hires to "
        "buy their own starter equipment upfront \u2014 that "
        "purchase is the actual scam, not a real onboarding step."
    )
    economy2_step1_b_feedback = (
        "Correct. Verifying through the company's own official "
        "careers page, separate from the recruiter who contacted "
        "you, is how you catch a fake hiring process."
    )
    economy2_step2_a_feedback = (
        "Correct. Declining and reporting the fake recruiter profile "
        "protects others being targeted with the same offer."
    )
    economy2_step2_b_feedback = (
        "Risky. A process \"feeling professional\" doesn't confirm "
        "it's real \u2014 that polish is often deliberate."
    )

    shopping2_step1_a_feedback = (
        "Risky. Moving payment off the marketplace removes any "
        "buyer protection you'd otherwise have \u2014 sellers who "
        "push for this are a strong warning sign, however "
        "convincing their reviews look."
    )
    shopping2_step1_b_feedback = (
        "Correct. Insisting on the platform's own checkout keeps "
        "your payment protected no matter how the seller frames "
        "the request."
    )
    shopping2_step2_a_feedback = (
        "Correct. Reporting the seller for requesting off-platform "
        "payment helps the marketplace warn or remove them before "
        "more buyers are affected."
    )
    shopping2_step2_b_feedback = (
        "Risky. Not reporting it leaves other buyers exposed to "
        "the same request."
    )

    government2_step1_a_feedback = (
        "Risky. Entering bank details to \"receive\" a refund is "
        "backwards \u2014 tax authorities don't need your account "
        "info to pay you, and this step is really about stealing "
        "it."
    )
    government2_step1_b_feedback = (
        "Correct. Checking directly on the tax authority's real "
        "site, not the emailed link, is the only reliable way to "
        "confirm a refund actually exists."
    )
    government2_step2_a_feedback = (
        "Correct. Reporting the phishing attempt helps the tax "
        "authority warn others receiving the same fake email."
    )
    government2_step2_b_feedback = (
        "Risky. \"Refunds like this do happen\" is true in general, "
        "but doesn't justify skipping verification on this "
        "specific one."
    )

    gaming2_step1_a_feedback = (
        "Risky. This mirrors a real-world OTP scam inside a gaming "
        "context \u2014 official support never needs you to read a "
        "verification code out to anyone, moderator or not."
    )
    gaming2_step1_b_feedback = (
        "Correct. Checking official support channels directly "
        "confirms whether any flag on your account is real, "
        "without trusting the DM at all."
    )
    gaming2_step2_a_feedback = (
        "Correct. Reporting the impersonating account helps "
        "moderators remove it before others are targeted."
    )
    gaming2_step2_b_feedback = (
        "Risky. Not reporting it leaves the same impersonation "
        "account free to target other members."
    )

    adaptive_start_a_feedback = (
        "Risky. Handing over the code under time pressure is "
        "exactly what this call is designed to get \u2014 real "
        "banks don't need you to read codes to \"lock out\" anyone."
    )
    adaptive_start_b_feedback = (
        "Correct. Refusing to act under pressure and checking "
        "independently is the right instinct \u2014 watch how the "
        "caller responds next."
    )
    adaptive_turn2_resisted_a_feedback = (
        "Risky. The caller switched from urgency to a policy threat "
        "\u2014 same goal, different lever. Complying still hands "
        "over control of the call."
    )
    adaptive_turn2_resisted_b_feedback = (
        "Correct. Asking for verifiable credentials and insisting "
        "on calling back through your own known number keeps you "
        "in control."
    )
    adaptive_turn2_gave_code_a_feedback = (
        "Risky. Having succeeded once, the attacker escalates to "
        "the next piece of information \u2014 this is the pattern "
        "worth recognizing: one success invites another ask."
    )
    adaptive_turn2_gave_code_b_feedback = (
        "Safer, but the first code is already given \u2014 hesitating "
        "now limits further damage without undoing what's already "
        "happened."
    )
    adaptive_final_safe_a_feedback = (
        "Correct. Reporting and adding extra protection closes the "
        "loop even though nothing was actually compromised this time."
    )
    adaptive_final_safe_b_feedback = (
        "Risky. Not reporting an attempted scam means your bank "
        "can't flag or warn against the same caller."
    )
    adaptive_final_risky_a_feedback = (
        "Correct. Freezing the card and changing your PIN limits "
        "further damage now that real details were exposed."
    )
    adaptive_final_risky_b_feedback = (
        "Risky. A blocked attempt doesn't mean your details are "
        "safe going forward \u2014 leaving them unchanged invites "
        "another attempt."
    )
    adaptive_final_partial_a_feedback = (
        "Correct. Changing your password after any partial exposure "
        "closes the door before it's tested further."
    )
    adaptive_final_partial_b_feedback = (
        "Risky. \"Nothing further happened\" this time doesn't mean "
        "the exposed code can't be reused or sold on."
    )

    return {
        "finance-otp-1": {
            "id": "finance-otp-1",
            "category": "finance",
            "title": "Unexpected bank text",
            "difficulty": "Beginner",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "SMS from \"GTBank Alert\": Your account will be "
                        "suspended in 24hrs due to unusual activity. "
                        "Verify now: bit.ly/gtb-secure123"
                    ),
                    "choices": [
                        {"id": "a", "text": "Click the link and verify immediately", "safe": False, "skill": "pressure", "feedback": step1_choice_a_feedback},
                        {"id": "b", "text": "Ignore the text and do nothing", "safe": False, "skill": "redflag", "feedback": step1_choice_b_feedback},
                        {"id": "c", "text": "Call your bank using the number on your card or official app", "safe": True, "skill": "verification", "feedback": step1_choice_c_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "You call your bank's official line. The "
                        "representative says there's no issue with your "
                        "account and no such message was sent by them."
                    ),
                    "choices": [
                        {"id": "a", "text": "Report the text as phishing and delete it", "safe": True, "skill": "decision", "feedback": step2_choice_a_feedback},
                        {"id": "b", "text": "Text back asking who sent it", "safe": False, "skill": "reasoning", "feedback": step2_choice_b_feedback}
                    ]
                }
            ]
        },
        "finance-otp-2": {
            "id": "finance-otp-2",
            "category": "finance",
            "title": "The fraud department call",
            "difficulty": "Advanced",
            "mode": "voice",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "A caller claiming to be your bank's fraud "
                        "department says: \"We've blocked a \u20a6450,000 "
                        "transfer attempt on your account. To fully "
                        "reverse it and secure your account, we're "
                        "sending you a verification code \u2014 please "
                        "read it back to us now.\" Moments later, a real "
                        "SMS with a 6-digit code arrives from your bank's "
                        "genuine number."
                    ),
                    "choices": [
                        {"id": "a", "text": "Read the code back to them since they're stopping fraud", "safe": False, "skill": "credential", "feedback": finance2_step1_a_feedback},
                        {"id": "b", "text": "Hang up and call your bank's official fraud line yourself", "safe": True, "skill": "verification", "feedback": finance2_step1_b_feedback},
                        {"id": "c", "text": "Stay on the line and check your banking app while they wait", "safe": False, "skill": "redflag", "feedback": finance2_step1_c_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "Your bank's real fraud line confirms there was "
                        "no blocked transaction \u2014 the code was for "
                        "a withdrawal the caller was attempting on your "
                        "account."
                    ),
                    "choices": [
                        {"id": "a", "text": "Report the incident and change your PIN and banking password", "safe": True, "skill": "decision", "feedback": finance2_step2_a_feedback},
                        {"id": "b", "text": "Assume it's resolved now that you didn't confirm the transfer", "safe": False, "skill": "reasoning", "feedback": finance2_step2_b_feedback}
                    ]
                }
            ]
        },
        "finance-adaptive-1": {
            "id": "finance-adaptive-1",
            "category": "finance",
            "title": "The adaptive security call",
            "difficulty": "Expert",
            "mode": "voice",
            "adaptive": True,
            "steps": {
                "start": {
                    "id": "start",
                    "message": (
                        "\"Hi, this is David calling from your bank's "
                        "security team. We've noticed a large "
                        "withdrawal attempt from your account just "
                        "now \u2014 was this you?\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "\"No, that wasn't me \u2014 what's happening?!\"",
                            "safe": False,
                            "skill": "pressure",
                            "feedback": (
                                "Reacting with visible alarm is natural, "
                                "but it signals to the caller that "
                                "pressure works on you \u2014 watch "
                                "what happens next."
                            ),
                            "next": "urgency_path"
                        },
                        {
                            "id": "b",
                            "text": "\"I don't recognize this number. Who exactly is calling?\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Good instinct to question the caller's "
                                "identity rather than react to the "
                                "claim itself \u2014 but the "
                                "conversation isn't over yet."
                            ),
                            "next": "authority_path"
                        },
                        {
                            "id": "c",
                            "text": "\"I'm going to hang up and call the bank directly to check.\"",
                            "safe": True,
                            "skill": "decision",
                            "feedback": (
                                "This ends the interaction immediately "
                                "and safely, before the caller gets "
                                "any chance to adapt. There was no "
                                "real security issue \u2014 this was a "
                                "simulated adaptive attacker testing "
                                "how quickly you'd disengage."
                            )
                        }
                    ]
                },
                "urgency_path": {
                    "id": "urgency_path",
                    "message": (
                        "\"I understand this is alarming \u2014 we "
                        "need to act fast before more money is taken. "
                        "I'm going to read you a verification code "
                        "that was just sent to your phone. Read it "
                        "back to me right now so I can freeze the "
                        "transaction.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "\"Okay, here's the code...\"",
                            "safe": False,
                            "skill": "credential",
                            "feedback": (
                                "The caller escalated straight to "
                                "urgency once you showed concern, and "
                                "it worked \u2014 that code almost "
                                "certainly authorized a transaction on "
                                "the attacker's end, not a freeze on "
                                "yours. This is exactly how adaptive "
                                "social engineering operates: no fixed "
                                "script, just reading your reaction "
                                "and pushing on it."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"Wait \u2014 I want to call the bank myself first.\"",
                            "safe": True,
                            "skill": "pressure",
                            "feedback": (
                                "You caught yourself and refused to "
                                "hand over the code. Notice the caller "
                                "only escalated to this level once "
                                "your first reaction showed concern "
                                "\u2014 that's the adaptive part. "
                                "Disengaging even earlier keeps you "
                                "further from ever reaching this point."
                            )
                        }
                    ]
                },
                "authority_path": {
                    "id": "authority_path",
                    "message": (
                        "\"Totally understand the caution \u2014 you "
                        "can find my employee ID, 44210, listed on our "
                        "website's security page. I just need you to "
                        "confirm your date of birth and the last 4 "
                        "digits of your card so I can pull up your "
                        "file.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "\"Okay, here's my information...\"",
                            "safe": False,
                            "skill": "credential",
                            "feedback": (
                                "Skepticism about the caller's "
                                "identity was the right start, but a "
                                "confident-sounding fake credential "
                                "(an employee ID you can't actually "
                                "verify) was enough to walk that "
                                "skepticism back. The caller adapted "
                                "their pitch specifically because your "
                                "first response was doubt, not fear."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"I'll verify that myself by calling the number on the back of my card.\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Holding your ground even after a "
                                "confident-sounding credential is "
                                "exactly right \u2014 a real employee "
                                "ID doesn't change the fact that you "
                                "should verify independently, not "
                                "through the same call."
                            )
                        }
                    ]
                }
            }
        },
        "work-bec-1": {
            "id": "work-bec-1",
            "category": "work",
            "title": "Urgent email from the CEO",
            "difficulty": "Intermediate",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "Email from \"CEO \u2014 Urgent\": I'm in back-to-back "
                        "meetings. Need you to buy $500 in Apple gift cards "
                        "for a client and send me the codes. Handle it "
                        "quietly, don't call me right now."
                    ),
                    "choices": [
                        {"id": "a", "text": "Buy the gift cards now and email the codes", "safe": False, "skill": "pressure", "feedback": work_step1_a_feedback},
                        {"id": "b", "text": "Reply to the email asking for more details", "safe": False, "skill": "verification", "feedback": work_step1_b_feedback},
                        {"id": "c", "text": "Message or call the CEO directly through a known, separate channel", "safe": True, "skill": "verification", "feedback": work_step1_c_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "You reach the real CEO, who confirms they never "
                        "sent this and have been in the office all day."
                    ),
                    "choices": [
                        {"id": "a", "text": "Report it to IT/security and forward the email", "safe": True, "skill": "decision", "feedback": work_step2_a_feedback},
                        {"id": "b", "text": "Delete it and don't mention it to anyone", "safe": False, "skill": "reasoning", "feedback": work_step2_b_feedback}
                    ]
                }
            ]
        },
        "work-bec-2": {
            "id": "work-bec-2",
            "category": "work",
            "title": "The vendor bank detail change",
            "difficulty": "Advanced",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "Email from your regular vendor, referencing "
                        "your real outstanding invoice #4482, from a "
                        "domain that looks right at a glance: \"Please "
                        "note we've changed our bank details effective "
                        "this week. Kindly update your records and send "
                        "this month's payment to the new account below "
                        "before Friday's deadline.\""
                    ),
                    "choices": [
                        {"id": "a", "text": "Update the details and pay to the new account before the deadline", "safe": False, "skill": "verification", "feedback": work2_step1_a_feedback},
                        {"id": "b", "text": "Call the vendor's known contact number, not one in the email, to confirm", "safe": True, "skill": "verification", "feedback": work2_step1_b_feedback},
                        {"id": "c", "text": "Reply to the email asking them to confirm the change in writing", "safe": False, "skill": "redflag", "feedback": work2_step1_c_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "The vendor's real accounts contact confirms "
                        "they never sent this and their bank details "
                        "haven't changed."
                    ),
                    "choices": [
                        {"id": "a", "text": "Report the email to finance and flag the suspicious domain", "safe": True, "skill": "decision", "feedback": work2_step2_a_feedback},
                        {"id": "b", "text": "Delete it and don't mention it to anyone", "safe": False, "skill": "reasoning", "feedback": work2_step2_b_feedback}
                    ]
                }
            ]
        },
        "work-adaptive-1": {
            "id": "work-adaptive-1",
            "category": "work",
            "title": "The IT security call",
            "difficulty": "Expert",
            "mode": "voice",
            "adaptive": True,
            "steps": {
                "start": {
                    "id": "start",
                    "message": (
                        "\"Hi, this is Daniel from IT Support. We've "
                        "detected suspicious login attempts on your "
                        "work account from an unrecognized device. Can "
                        "you confirm this wasn't you?\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "\"No! Is my account compromised?!\"",
                            "safe": False,
                            "skill": "pressure",
                            "feedback": (
                                "Reacting with alarm is a natural "
                                "response, but it tells the caller "
                                "exactly which lever to pull next."
                            ),
                            "next": "urgency_path"
                        },
                        {
                            "id": "b",
                            "text": "\"I wasn't told IT would be calling about this. What's your extension?\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Asking for something checkable is the "
                                "right move \u2014 but the caller isn't "
                                "done yet."
                            ),
                            "next": "authority_path"
                        },
                        {
                            "id": "c",
                            "text": "\"I'll check this myself through the IT help desk portal.\"",
                            "safe": True,
                            "skill": "decision",
                            "feedback": (
                                "Ending the call here and verifying "
                                "independently is the strongest "
                                "possible response \u2014 the caller "
                                "never gets a chance to adapt."
                            )
                        }
                    ]
                },
                "urgency_path": {
                    "id": "urgency_path",
                    "message": (
                        "\"We need to lock this down immediately "
                        "before they access company data. I'm sending "
                        "an MFA push to your phone \u2014 just approve "
                        "it so I can force a password reset from our "
                        "side.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "Approve the MFA push",
                            "safe": False,
                            "skill": "credential",
                            "feedback": (
                                "Approving a push you didn't request "
                                "grants the attacker access directly "
                                "\u2014 real IT never needs you to "
                                "approve a login prompt you didn't "
                                "initiate yourself."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"I'll call the help desk main line to confirm before approving anything.\"",
                            "safe": True,
                            "skill": "pressure",
                            "feedback": (
                                "Refusing to approve an unrequested "
                                "prompt, even under urgency, is exactly "
                                "right \u2014 the escalation only came "
                                "because your first reaction showed "
                                "concern."
                            )
                        }
                    ]
                },
                "authority_path": {
                    "id": "authority_path",
                    "message": (
                        "\"Understandable \u2014 my extension is 4471, "
                        "you can look me up in the directory. While I "
                        "have you, can you just confirm your employee "
                        "ID and current password so I can verify you "
                        "in our system?\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "Give your employee ID and password",
                            "safe": False,
                            "skill": "credential",
                            "feedback": (
                                "No legitimate IT process ever needs "
                                "your actual password, full stop \u2014 "
                                "a checkable extension doesn't change "
                                "that rule."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"IT would never ask for my password \u2014 I'm ending this call and reporting it.\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Holding that line even after the "
                                "caller offered a verifiable-sounding "
                                "detail is exactly the right instinct."
                            )
                        }
                    ]
                }
            }
        },
        "social-verify-1": {
            "id": "social-verify-1",
            "category": "social",
            "title": "Account verification DM",
            "difficulty": "Intermediate",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "DM from \"Support Team\" (unverified account): "
                        "Your account will be permanently deleted in 12 "
                        "hours for policy violations. Confirm your "
                        "identity now: secure-verify-account.net/login"
                    ),
                    "choices": [
                        {"id": "a", "text": "Log in through the link to confirm your identity", "safe": False, "skill": "credential", "feedback": social_step1_a_feedback},
                        {"id": "b", "text": "Open the real app directly and check your account status there", "safe": True, "skill": "redflag", "feedback": social_step1_b_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "Inside the real app, your account shows no "
                        "warnings, restrictions, or pending issues."
                    ),
                    "choices": [
                        {"id": "a", "text": "Block the account and report the DM", "safe": True, "skill": "decision", "feedback": social_step2_a_feedback},
                        {"id": "b", "text": "Reply asking what policy you violated", "safe": False, "skill": "manipulation", "feedback": social_step2_b_feedback}
                    ]
                }
            ]
        },
        "social-verify-2": {
            "id": "social-verify-2",
            "category": "social",
            "title": "The friend's locked-out account",
            "difficulty": "Advanced",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "Message from a friend's account (handle has "
                        "one extra letter you don't immediately "
                        "notice): \"Hey, I'm locked out of my account. "
                        "Can you help? I'll have them send a code to "
                        "your phone since mine's down, just forward it "
                        "to me when it comes.\""
                    ),
                    "choices": [
                        {"id": "a", "text": "Agree and forward the code once it arrives", "safe": False, "skill": "redflag", "feedback": social2_step1_a_feedback},
                        {"id": "b", "text": "Contact your friend a different, already-known way to confirm it's really them", "safe": True, "skill": "verification", "feedback": social2_step1_b_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "You reach your actual friend a different way "
                        "\u2014 they never sent that message, and their "
                        "account appears to have been compromised."
                    ),
                    "choices": [
                        {"id": "a", "text": "Warn shared contacts and report the fake account", "safe": True, "skill": "decision", "feedback": social2_step2_a_feedback},
                        {"id": "b", "text": "Do nothing since your own account wasn't affected", "safe": False, "skill": "reasoning", "feedback": social2_step2_b_feedback}
                    ]
                }
            ]
        },
        "social-adaptive-1": {
            "id": "social-adaptive-1",
            "category": "social",
            "title": "The trust and safety DM",
            "difficulty": "Expert",
            "adaptive": True,
            "steps": {
                "start": {
                    "id": "start",
                    "message": (
                        "\"This is Alex from Platform Trust & Safety. "
                        "We noticed a login from a new device in "
                        "another country. Was this you?\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "\"No! Someone hacked me?!\"",
                            "safe": False,
                            "skill": "pressure",
                            "feedback": (
                                "Alarm is a natural reaction, but it "
                                "signals exactly which angle the "
                                "sender will push next."
                            ),
                            "next": "urgency_path"
                        },
                        {
                            "id": "b",
                            "text": "\"Trust & Safety doesn't DM users first for this. Prove you're legit.\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Questioning the channel itself is the "
                                "right start \u2014 but the "
                                "conversation isn't over."
                            ),
                            "next": "authority_path"
                        },
                        {
                            "id": "c",
                            "text": "\"I'll check my login activity myself in the app's settings.\"",
                            "safe": True,
                            "skill": "decision",
                            "feedback": (
                                "Verifying independently and ending "
                                "the DM here is the strongest possible "
                                "response \u2014 there's nothing left "
                                "for the sender to adapt to."
                            )
                        }
                    ]
                },
                "urgency_path": {
                    "id": "urgency_path",
                    "message": (
                        "\"I know it's stressful \u2014 to lock the "
                        "account before they change your password, I "
                        "need the reset code we just sent you. Send it "
                        "now so I can secure it on my end.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "Send the reset code",
                            "safe": False,
                            "skill": "credential",
                            "feedback": (
                                "That reset code is what actually "
                                "hands over your account \u2014 the "
                                "\"help\" being offered is the attack "
                                "itself."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"I'll reset it myself through the app, not through you.\"",
                            "safe": True,
                            "skill": "pressure",
                            "feedback": (
                                "Refusing to hand over the code, even "
                                "framed as help, is exactly right."
                            )
                        }
                    ]
                },
                "authority_path": {
                    "id": "authority_path",
                    "message": (
                        "\"Fair question \u2014 here's a screenshot of "
                        "my staff badge. I just need you to confirm "
                        "the email on file and the reset code so I can "
                        "lock down the account from here.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "Confirm the email and reset code",
                            "safe": False,
                            "skill": "credential",
                            "feedback": (
                                "A screenshot proves nothing \u2014 "
                                "it's trivial to fake, and real staff "
                                "never need your reset code regardless "
                                "of how official they look."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"Real staff never need my reset code. I'm reporting this and changing my password myself.\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Holding the line on the actual rule, "
                                "not the appearance of legitimacy, is "
                                "exactly right."
                            )
                        }
                    ]
                }
            }
        },
        "education-scholarship-1": {
            "id": "education-scholarship-1",
            "category": "education",
            "title": "The scholarship email",
            "difficulty": "Beginner",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "Email from \"National Merit Scholarship Board\": "
                        "\"Congratulations! You've been selected for a "
                        "\u20a6250,000 scholarship. To claim it, pay a "
                        "\u20a615,000 processing fee within 24 hours via "
                        "the link below.\""
                    ),
                    "choices": [
                        {"id": "a", "text": "Pay the fee immediately to secure the scholarship", "safe": False, "skill": "redflag", "feedback": education_step1_a_feedback},
                        {"id": "b", "text": "Search for the board's official site and verify independently", "safe": True, "skill": "verification", "feedback": education_step1_b_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "You find no record of this scholarship board "
                        "anywhere, and the real Ministry of Education "
                        "site has no listing for it."
                    ),
                    "choices": [
                        {"id": "a", "text": "Report the email as a scam and don't pay", "safe": True, "skill": "decision", "feedback": education_step2_a_feedback},
                        {"id": "b", "text": "Pay anyway since it's a relatively small amount", "safe": False, "skill": "reasoning", "feedback": education_step2_b_feedback}
                    ]
                }
            ]
        },
        "education-scholarship-2": {
            "id": "education-scholarship-2",
            "category": "education",
            "title": "The interview verification deposit",
            "difficulty": "Advanced",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "Email referencing a real exchange program you "
                        "applied to: \"Your application has advanced to "
                        "the interview stage. To confirm your slot, a "
                        "refundable $50 verification deposit is "
                        "required via the portal link below within 48 "
                        "hours.\""
                    ),
                    "choices": [
                        {"id": "a", "text": "Pay the deposit through the link to confirm your slot", "safe": False, "skill": "verification", "feedback": education2_step1_a_feedback},
                        {"id": "b", "text": "Log into the university's official portal directly to check", "safe": True, "skill": "verification", "feedback": education2_step1_b_feedback},
                        {"id": "c", "text": "Call the number in the email's signature to confirm", "safe": False, "skill": "redflag", "feedback": education2_step1_c_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "Logging into the official portal directly, "
                        "there's no interview stage or deposit "
                        "requirement mentioned anywhere in your "
                        "application status."
                    ),
                    "choices": [
                        {"id": "a", "text": "Report the email to the university's IT/security office", "safe": True, "skill": "decision", "feedback": education2_step2_a_feedback},
                        {"id": "b", "text": "Assume it's a new requirement they forgot to list, and pay anyway", "safe": False, "skill": "reasoning", "feedback": education2_step2_b_feedback}
                    ]
                }
            ]
        },
        "education-adaptive-1": {
            "id": "education-adaptive-1",
            "category": "education",
            "title": "The financial aid call",
            "difficulty": "Expert",
            "mode": "voice",
            "adaptive": True,
            "steps": {
                "start": {
                    "id": "start",
                    "message": (
                        "\"Hi, this is Sarah calling from the "
                        "Financial Aid Office. There's a discrepancy "
                        "in your enrollment status that could affect "
                        "your aid \u2014 can you confirm you're still "
                        "enrolled?\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "\"Wait, is my aid at risk?!\"",
                            "safe": False,
                            "skill": "pressure",
                            "feedback": (
                                "Concern about your aid is a natural "
                                "reaction, but it tells the caller "
                                "exactly how to escalate next."
                            ),
                            "next": "urgency_path"
                        },
                        {
                            "id": "b",
                            "text": "\"I haven't heard about this from the school. What department are you with?\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Asking for a specific, checkable "
                                "detail is the right instinct \u2014 "
                                "but the call isn't over."
                            ),
                            "next": "authority_path"
                        },
                        {
                            "id": "c",
                            "text": "\"I'll check my enrollment status directly through the student portal.\"",
                            "safe": True,
                            "skill": "decision",
                            "feedback": (
                                "Ending the call and verifying "
                                "independently is the strongest "
                                "response \u2014 there's nothing left "
                                "for the caller to adapt to."
                            )
                        }
                    ]
                },
                "urgency_path": {
                    "id": "urgency_path",
                    "message": (
                        "\"I understand the stress \u2014 to resolve "
                        "this before today's deadline, I just need you "
                        "to verify your student ID and social security "
                        "number so I can update your file.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "Give your student ID and social security number",
                            "safe": False,
                            "skill": "credential",
                            "feedback": (
                                "A deadline framed as urgent is the "
                                "pressure tactic itself \u2014 no "
                                "financial aid office needs your SSN "
                                "read out over an unexpected call."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"I'll go through the financial aid portal myself instead.\"",
                            "safe": True,
                            "skill": "pressure",
                            "feedback": (
                                "Refusing to act on the deadline "
                                "pressure and verifying independently "
                                "instead is exactly right."
                            )
                        }
                    ]
                },
                "authority_path": {
                    "id": "authority_path",
                    "message": (
                        "\"Fair enough \u2014 I'm with the Enrollment "
                        "Compliance division, listed under Financial "
                        "Aid. I just need your student ID and date of "
                        "birth to pull up your file and fix this "
                        "today.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "Give your student ID and date of birth",
                            "safe": False,
                            "skill": "credential",
                            "feedback": (
                                "A department name that sounds "
                                "official doesn't confirm anything "
                                "\u2014 the caller adapted specifically "
                                "because your first question was "
                                "skepticism, not fear."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"I'll call the financial aid office's main line myself to check this.\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Verifying through a number you "
                                "already trust, not the one that "
                                "called you, is exactly right."
                            )
                        }
                    ]
                }
            }
        },
        "economy-grant-1": {
            "id": "economy-grant-1",
            "category": "economy",
            "title": "The empowerment grant message",
            "difficulty": "Beginner",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "WhatsApp message: \"FEDERAL GOVERNMENT "
                        "EMPOWERMENT GRANT: You've been selected to "
                        "receive \u20a6100,000 under the Youth Empowerment "
                        "Scheme. Send your BVN and a \u20a62,000 "
                        "registration fee to claim.\""
                    ),
                    "choices": [
                        {"id": "a", "text": "Send your BVN and pay the fee to claim it", "safe": False, "skill": "credential", "feedback": economy_step1_a_feedback},
                        {"id": "b", "text": "Ignore it \u2014 real grants don't ask for your BVN or a fee this way", "safe": True, "skill": "redflag", "feedback": economy_step1_b_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "You check the real government scheme's website. "
                        "There's no such registration process, and it "
                        "explicitly warns against messages just like "
                        "this one."
                    ),
                    "choices": [
                        {"id": "a", "text": "Block the sender and warn others about the pattern", "safe": True, "skill": "decision", "feedback": economy_step2_a_feedback},
                        {"id": "b", "text": "Reply asking for \"proof\" before deciding", "safe": False, "skill": "manipulation", "feedback": economy_step2_b_feedback}
                    ]
                }
            ]
        },
        "economy-grant-2": {
            "id": "economy-grant-2",
            "category": "economy",
            "title": "The starter kit job offer",
            "difficulty": "Advanced",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "A recruiter claims to be hiring remotely for "
                        "a well-known company. After a brief text "
                        "\"interview,\" they say: \"Congratulations, "
                        "you're hired! To receive your starter kit and "
                        "account access, purchase a $150 training kit "
                        "from our approved vendor \u2014 it'll be "
                        "refunded in your first paycheck.\""
                    ),
                    "choices": [
                        {"id": "a", "text": "Purchase the training kit to secure the job", "safe": False, "skill": "redflag", "feedback": economy2_step1_a_feedback},
                        {"id": "b", "text": "Check the company's official careers page and contact them directly", "safe": True, "skill": "verification", "feedback": economy2_step1_b_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "The company's official careers page confirms "
                        "they never ask new hires to purchase "
                        "equipment upfront, and a search turns up many "
                        "reports of this exact scam using their name."
                    ),
                    "choices": [
                        {"id": "a", "text": "Decline the \"job\" and report the recruiter's profile", "safe": True, "skill": "decision", "feedback": economy2_step2_a_feedback},
                        {"id": "b", "text": "Pay anyway since the interview felt professional", "safe": False, "skill": "reasoning", "feedback": economy2_step2_b_feedback}
                    ]
                }
            ]
        },
        "economy-adaptive-1": {
            "id": "economy-adaptive-1",
            "category": "economy",
            "title": "The grant review call",
            "difficulty": "Expert",
            "mode": "voice",
            "adaptive": True,
            "steps": {
                "start": {
                    "id": "start",
                    "message": (
                        "\"Hi, this is Michael from the National Youth "
                        "Empowerment Program. Your application for the "
                        "\u20a6150,000 grant has been flagged for "
                        "review \u2014 are you still interested in "
                        "receiving it?\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "\"Yes! What do I need to do to fix it?!\"",
                            "safe": False,
                            "skill": "manipulation",
                            "feedback": (
                                "Eagerness to fix the flag is a "
                                "natural response, but it signals "
                                "exactly which angle to push next."
                            ),
                            "next": "urgency_path"
                        },
                        {
                            "id": "b",
                            "text": "\"I don't remember applying. Which office are you calling from?\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Questioning whether you even applied "
                                "is a strong start \u2014 but the "
                                "caller isn't finished."
                            ),
                            "next": "authority_path"
                        },
                        {
                            "id": "c",
                            "text": "\"I'll check the program's official website myself for any updates.\"",
                            "safe": True,
                            "skill": "decision",
                            "feedback": (
                                "Ending the call and verifying "
                                "independently is the strongest "
                                "response available here."
                            )
                        }
                    ]
                },
                "urgency_path": {
                    "id": "urgency_path",
                    "message": (
                        "\"The review window closes today \u2014 I "
                        "just need you to confirm your BVN and pay a "
                        "\u20a63,000 verification fee to release the "
                        "funds.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "Pay the fee and give your BVN",
                            "safe": False,
                            "skill": "credential",
                            "feedback": (
                                "Real grants don't require your BVN or "
                                "a fee to be released \u2014 the "
                                "\"closing window\" is designed to "
                                "stop you from checking that."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"I'll check on the official site before paying anything.\"",
                            "safe": True,
                            "skill": "manipulation",
                            "feedback": (
                                "Refusing to act on the closing-window "
                                "pressure and verifying instead is "
                                "exactly right."
                            )
                        }
                    ]
                },
                "authority_path": {
                    "id": "authority_path",
                    "message": (
                        "\"I'm calling from the program's regional "
                        "office \u2014 you can find our number listed "
                        "if you search. I just need your BVN to "
                        "confirm eligibility so we can proceed.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "Give your BVN",
                            "safe": False,
                            "skill": "credential",
                            "feedback": (
                                "\"You can find us if you search\" "
                                "isn't the same as verifying through a "
                                "number you already trust \u2014 the "
                                "caller adapted the pitch specifically "
                                "because you were skeptical."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"Real government programs don't need my BVN over a phone call. I'll verify this myself.\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Holding that line regardless of how "
                                "the caller frames their legitimacy is "
                                "exactly right."
                            )
                        }
                    ]
                }
            }
        },
        "personal-romance-1": {
            "id": "personal-romance-1",
            "category": "personal",
            "title": "Emergency from an online partner",
            "difficulty": "Advanced",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "Message from someone you met online three weeks "
                        "ago, never in person: \"I'm stuck at customs and "
                        "they're holding my luggage until I pay a $600 "
                        "fee. Can you send it today? I'll pay you back "
                        "as soon as I land, I promise.\""
                    ),
                    "choices": [
                        {"id": "a", "text": "Send the money right away to help them", "safe": False, "skill": "manipulation", "feedback": personal_step1_a_feedback},
                        {"id": "b", "text": "Say you want to help, but ask to video call first to talk it through", "safe": True, "skill": "verification", "feedback": personal_step1_b_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "They reply: \"My camera's broken and there's "
                        "no time, please, I really need this right now.\""
                    ),
                    "choices": [
                        {"id": "a", "text": "Treat this as confirmation it's a scam and stop responding", "safe": True, "skill": "reasoning", "feedback": personal_step2_a_feedback},
                        {"id": "b", "text": "Send the money since they sound genuinely desperate", "safe": False, "skill": "pressure", "feedback": personal_step2_b_feedback}
                    ]
                }
            ]
        },
        "personal-romance-2": {
            "id": "personal-romance-2",
            "category": "personal",
            "title": "A sudden declaration",
            "difficulty": "Beginner",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "Someone you've never spoken to before "
                        "messages: \"Hi beautiful, I saw your profile "
                        "and I think we're meant to be together. I'm a "
                        "US Army general on a peacekeeping mission and "
                        "I need $2,000 for a plane ticket to come meet "
                        "you. Can you help your future husband?\""
                    ),
                    "choices": [
                        {"id": "a", "text": "Send the money to help your future husband", "safe": False, "skill": "manipulation", "feedback": personal2_step1_a_feedback},
                        {"id": "b", "text": "Block and report the account immediately", "safe": True, "skill": "redflag", "feedback": personal2_step1_b_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "You mention this to a friend, who immediately "
                        "recognizes the classic \"military romance "
                        "scam\" pattern from stories they've heard "
                        "before."
                    ),
                    "choices": [
                        {"id": "a", "text": "Confirm your decision to block/report and warn others", "safe": True, "skill": "decision", "feedback": personal2_step2_a_feedback},
                        {"id": "b", "text": "Feel bad and consider unblocking to at least talk", "safe": False, "skill": "reasoning", "feedback": personal2_step2_b_feedback}
                    ]
                }
            ]
        },
        "personal-adaptive-1": {
            "id": "personal-adaptive-1",
            "category": "personal",
            "title": "The sudden crisis call",
            "difficulty": "Expert",
            "mode": "voice",
            "adaptive": True,
            "steps": {
                "start": {
                    "id": "start",
                    "message": (
                        "\"Hey love, it's me. Something's wrong, I "
                        "really need to talk to you right now, are "
                        "you free?\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "\"Oh no, what's wrong?! Tell me everything.\"",
                            "safe": False,
                            "skill": "manipulation",
                            "feedback": (
                                "Wanting to help immediately is a "
                                "natural, caring response \u2014 but "
                                "it also signals exactly how to move "
                                "you."
                            ),
                            "next": "urgency_path"
                        },
                        {
                            "id": "b",
                            "text": "\"You sound upset \u2014 before anything else, can we video call so I can see you?\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Asking to see them before engaging "
                                "further is a strong instinct \u2014 "
                                "but the conversation isn't over yet."
                            ),
                            "next": "authority_path"
                        },
                        {
                            "id": "c",
                            "text": "\"I'm going to need some time before discussing anything serious \u2014 let's talk later.\"",
                            "safe": True,
                            "skill": "decision",
                            "feedback": (
                                "Setting a boundary and ending the "
                                "call here is the strongest possible "
                                "response \u2014 there's no opening "
                                "left for the caller to work with."
                            )
                        }
                    ]
                },
                "urgency_path": {
                    "id": "urgency_path",
                    "message": (
                        "\"I'm in trouble, I can't explain everything "
                        "right now but I need $800 wired today or "
                        "something really bad is going to happen. "
                        "Please, I wouldn't ask if it wasn't serious.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "Send the money",
                            "safe": False,
                            "skill": "pressure",
                            "feedback": (
                                "Vague, unverifiable urgency paired "
                                "with a direct money request is the "
                                "core of this scam \u2014 caring about "
                                "someone doesn't require skipping "
                                "verification."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"I need to understand exactly what's happening before I send anything.\"",
                            "safe": True,
                            "skill": "manipulation",
                            "feedback": (
                                "Refusing to act on vague urgency, "
                                "even from someone you care about, is "
                                "exactly right."
                            )
                        }
                    ]
                },
                "authority_path": {
                    "id": "authority_path",
                    "message": (
                        "\"My camera's broken right now, I promise "
                        "it's really me, you can trust me \u2014 I "
                        "just need you to send $800 today, it's an "
                        "emergency.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "Send the money",
                            "safe": False,
                            "skill": "manipulation",
                            "feedback": (
                                "A convenient excuse for refusing to "
                                "video call, right after you asked for "
                                "one, is itself a strong signal \u2014 "
                                "not a reason to skip verification."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"Until I can verify it's really you, I'm not sending anything.\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Holding your ground on verification, "
                                "even after a sympathetic excuse, is "
                                "exactly right."
                            )
                        }
                    ]
                }
            }
        },
        "shopping-delivery-1": {
            "id": "shopping-delivery-1",
            "category": "shopping",
            "title": "The unpaid delivery fee",
            "difficulty": "Beginner",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "SMS: \"Your package could not be delivered due "
                        "to an unpaid customs fee of \u20a61,500. Pay now "
                        "to reschedule delivery: track-ng-delivery.com/pay\""
                    ),
                    "choices": [
                        {"id": "a", "text": "Click the link and pay the fee right away", "safe": False, "skill": "redflag", "feedback": shopping_step1_a_feedback},
                        {"id": "b", "text": "Check the tracking number on the courier's official app or site", "safe": True, "skill": "verification", "feedback": shopping_step1_b_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "The courier's official app shows no pending "
                        "delivery, and your last order is already "
                        "marked delivered."
                    ),
                    "choices": [
                        {"id": "a", "text": "Report the SMS as a scam and delete it", "safe": True, "skill": "decision", "feedback": shopping_step2_a_feedback},
                        {"id": "b", "text": "Pay it anyway just in case it's real", "safe": False, "skill": "reasoning", "feedback": shopping_step2_b_feedback}
                    ]
                }
            ]
        },
        "shopping-delivery-2": {
            "id": "shopping-delivery-2",
            "category": "shopping",
            "title": "The off-platform payment request",
            "difficulty": "Advanced",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "A marketplace seller with several positive "
                        "reviews messages: \"To avoid the marketplace's "
                        "8% fee, let's just do this by bank transfer "
                        "directly. I'll ship as soon as I get payment, "
                        "it's honestly way easier for both of us.\""
                    ),
                    "choices": [
                        {"id": "a", "text": "Agree and pay by direct bank transfer outside the platform", "safe": False, "skill": "manipulation", "feedback": shopping2_step1_a_feedback},
                        {"id": "b", "text": "Decline and insist on paying through the marketplace's checkout", "safe": True, "skill": "redflag", "feedback": shopping2_step1_b_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "Days later, several other buyers post reviews "
                        "saying the same seller convinced them to pay "
                        "off-platform and then never shipped anything."
                    ),
                    "choices": [
                        {"id": "a", "text": "Report the seller to the marketplace for requesting off-platform payment", "safe": True, "skill": "decision", "feedback": shopping2_step2_a_feedback},
                        {"id": "b", "text": "Feel relieved you avoided it, but don't bother reporting", "safe": False, "skill": "reasoning", "feedback": shopping2_step2_b_feedback}
                    ]
                }
            ]
        },
        "shopping-adaptive-1": {
            "id": "shopping-adaptive-1",
            "category": "shopping",
            "title": "The payment verification call",
            "difficulty": "Expert",
            "mode": "voice",
            "adaptive": True,
            "steps": {
                "start": {
                    "id": "start",
                    "message": (
                        "\"Hi, this is Grace from Marketplace Support. "
                        "We've flagged unusual activity on your recent "
                        "order and need to verify your payment method "
                        "before it ships \u2014 is that alright?\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "\"Oh no, is something wrong with my order?!\"",
                            "safe": False,
                            "skill": "pressure",
                            "feedback": (
                                "Worrying about your order is natural, "
                                "but it tells the caller exactly how "
                                "to escalate next."
                            ),
                            "next": "urgency_path"
                        },
                        {
                            "id": "b",
                            "text": "\"Support usually messages through the app, not calls. What's my order number?\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Questioning the channel and asking "
                                "for a checkable detail is a strong "
                                "start \u2014 but the call continues."
                            ),
                            "next": "authority_path"
                        },
                        {
                            "id": "c",
                            "text": "\"I'll check my order status directly in the app.\"",
                            "safe": True,
                            "skill": "decision",
                            "feedback": (
                                "Ending the call and verifying inside "
                                "the app directly is the strongest "
                                "possible response here."
                            )
                        }
                    ]
                },
                "urgency_path": {
                    "id": "urgency_path",
                    "message": (
                        "\"To avoid your order being cancelled, I just "
                        "need your card number and the 3-digit code "
                        "on the back to re-verify the payment right "
                        "now.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "Give your card number and security code",
                            "safe": False,
                            "skill": "credential",
                            "feedback": (
                                "No legitimate marketplace needs your "
                                "full card number and security code "
                                "read out over a call \u2014 the "
                                "cancellation threat exists only to "
                                "rush you past that fact."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"I'll check the app myself instead of giving that over the phone.\"",
                            "safe": True,
                            "skill": "pressure",
                            "feedback": (
                                "Refusing to give card details under "
                                "cancellation pressure is exactly "
                                "right."
                            )
                        }
                    ]
                },
                "authority_path": {
                    "id": "authority_path",
                    "message": (
                        "\"It's order #58291 \u2014 I can see it in "
                        "our system. I just need you to confirm your "
                        "card details so I can clear the flag.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "Confirm your card details",
                            "safe": False,
                            "skill": "credential",
                            "feedback": (
                                "Knowing your order number doesn't "
                                "prove legitimacy \u2014 that "
                                "information can be seen or guessed "
                                "elsewhere, and it was offered "
                                "specifically because you asked for "
                                "proof."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"I'll verify this through the app's official support chat instead.\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Moving verification to a channel you "
                                "control, rather than trusting the "
                                "caller's claim, is exactly right."
                            )
                        }
                    ]
                }
            }
        },
        "government-immigration-1": {
            "id": "government-immigration-1",
            "category": "government",
            "title": "The immigration officer call",
            "difficulty": "Intermediate",
            "mode": "voice",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "Call from \"Immigration Officer\": \"There's an "
                        "issue with your travel documents. Pay a "
                        "\u20a620,000 processing fee immediately by "
                        "transfer or face arrest at your next travel "
                        "date.\""
                    ),
                    "choices": [
                        {"id": "a", "text": "Pay immediately to avoid arrest", "safe": False, "skill": "pressure", "feedback": government_step1_a_feedback},
                        {"id": "b", "text": "Hang up and contact the immigration office through their official number", "safe": True, "skill": "verification", "feedback": government_step1_b_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "The office's official line confirms there is "
                        "no issue with your documents, and that they "
                        "never request payment by phone."
                    ),
                    "choices": [
                        {"id": "a", "text": "Report the call to the relevant authorities", "safe": True, "skill": "decision", "feedback": government_step2_a_feedback},
                        {"id": "b", "text": "Ignore it completely since nothing happened", "safe": False, "skill": "reasoning", "feedback": government_step2_b_feedback}
                    ]
                }
            ]
        },
        "government-immigration-2": {
            "id": "government-immigration-2",
            "category": "government",
            "title": "The tax refund portal",
            "difficulty": "Advanced",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "Email styled like the tax authority: \"You are "
                        "eligible for a tax refund of \u20a685,000. To "
                        "process it, verify your bank account details "
                        "on our secure portal within 5 business days: "
                        "fira-taxrefund-portal.com\""
                    ),
                    "choices": [
                        {"id": "a", "text": "Enter your bank account details on the portal to claim it", "safe": False, "skill": "credential", "feedback": government2_step1_a_feedback},
                        {"id": "b", "text": "Log into the tax authority's actual official website directly", "safe": True, "skill": "verification", "feedback": government2_step1_b_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "Checking the real tax portal directly shows no "
                        "refund pending, and no bank verification "
                        "request was ever issued."
                    ),
                    "choices": [
                        {"id": "a", "text": "Report the email as phishing to the tax authority and delete it", "safe": True, "skill": "decision", "feedback": government2_step2_a_feedback},
                        {"id": "b", "text": "Enter the details anyway since refunds like this do happen", "safe": False, "skill": "reasoning", "feedback": government2_step2_b_feedback}
                    ]
                }
            ]
        },
        "government-adaptive-1": {
            "id": "government-adaptive-1",
            "category": "government",
            "title": "The tax audit call",
            "difficulty": "Expert",
            "mode": "voice",
            "adaptive": True,
            "steps": {
                "start": {
                    "id": "start",
                    "message": (
                        "\"This is Officer Bello calling from the Tax "
                        "Authority. Our records show a discrepancy in "
                        "your last filing that requires immediate "
                        "attention \u2014 are you aware of this?\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "\"No! Am I in trouble?!\"",
                            "safe": False,
                            "skill": "pressure",
                            "feedback": (
                                "Worry about being in trouble is a "
                                "natural reaction, but it signals "
                                "exactly how to escalate next."
                            ),
                            "next": "urgency_path"
                        },
                        {
                            "id": "b",
                            "text": "\"The tax authority doesn't usually call directly about this. What's your badge number?\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Questioning the channel and asking "
                                "for a checkable identifier is the "
                                "right start \u2014 but the call "
                                "continues."
                            ),
                            "next": "authority_path"
                        },
                        {
                            "id": "c",
                            "text": "\"I'll check my filing status directly through the official tax portal.\"",
                            "safe": True,
                            "skill": "decision",
                            "feedback": (
                                "Ending the call and verifying "
                                "directly through the official portal "
                                "is the strongest response available."
                            )
                        }
                    ]
                },
                "urgency_path": {
                    "id": "urgency_path",
                    "message": (
                        "\"To resolve this before penalties apply "
                        "today, I need you to make a payment now via "
                        "bank transfer to clear the discrepancy.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "Make the payment",
                            "safe": False,
                            "skill": "pressure",
                            "feedback": (
                                "Real tax authorities never resolve "
                                "discrepancies through an immediate "
                                "phone transfer \u2014 the same-day "
                                "penalty threat exists purely to rush "
                                "that decision."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"I'll verify this through the official tax portal myself before paying anything.\"",
                            "safe": True,
                            "skill": "pressure",
                            "feedback": (
                                "Refusing to pay under same-day "
                                "penalty pressure and verifying "
                                "independently is exactly right."
                            )
                        }
                    ]
                },
                "authority_path": {
                    "id": "authority_path",
                    "message": (
                        "\"Badge number 2214, you can note that down. "
                        "I just need your tax ID and bank account "
                        "number to process the correction.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "Give your tax ID and bank account number",
                            "safe": False,
                            "skill": "credential",
                            "feedback": (
                                "A badge number you can't actually "
                                "verify doesn't justify handing over "
                                "your bank account \u2014 it was "
                                "offered specifically because you "
                                "asked for proof."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"I'll go through the official portal directly instead of giving that over the phone.\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Holding that line and verifying "
                                "through the real portal, not the "
                                "caller's claim, is exactly right."
                            )
                        }
                    ]
                }
            }
        },
        "gaming-rewards-1": {
            "id": "gaming-rewards-1",
            "category": "gaming",
            "title": "The free gems giveaway",
            "difficulty": "Beginner",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "In-game chat message: \"Free 5000 gems for the "
                        "next 10 minutes only! Just login with your "
                        "username and password here to claim: "
                        "gamerewards-free.net\""
                    ),
                    "choices": [
                        {"id": "a", "text": "Log in through the link to claim the free gems", "safe": False, "skill": "credential", "feedback": gaming_step1_a_feedback},
                        {"id": "b", "text": "Ignore it \u2014 games don't give rewards through third-party login links", "safe": True, "skill": "redflag", "feedback": gaming_step1_b_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "The official game's news page shows no such "
                        "promotion, and explicitly warns against sites "
                        "like this stealing accounts."
                    ),
                    "choices": [
                        {"id": "a", "text": "Report the message in-game and keep your login private", "safe": True, "skill": "decision", "feedback": gaming_step2_a_feedback},
                        {"id": "b", "text": "Try it anyway since it's \"just a game account\"", "safe": False, "skill": "reasoning", "feedback": gaming_step2_b_feedback}
                    ]
                }
            ]
        },
        "gaming-rewards-2": {
            "id": "gaming-rewards-2",
            "category": "gaming",
            "title": "The account flag DM",
            "difficulty": "Advanced",
            "steps": [
                {
                    "id": 1,
                    "message": (
                        "Someone in your gaming Discord, using a name "
                        "close to a known moderator's, DMs you: \"We've "
                        "flagged unusual activity on your account. To "
                        "verify it's really you, support will send a "
                        "code to your email \u2014 read it to me here "
                        "so I can lift the flag.\""
                    ),
                    "choices": [
                        {"id": "a", "text": "Read the code to them once it arrives", "safe": False, "skill": "credential", "feedback": gaming2_step1_a_feedback},
                        {"id": "b", "text": "Check official support channels directly for any real flag", "safe": True, "skill": "verification", "feedback": gaming2_step1_b_feedback}
                    ]
                },
                {
                    "id": 2,
                    "message": (
                        "Official support confirms there is no flag on "
                        "your account, and that staff never ask for "
                        "verification codes through DMs."
                    ),
                    "choices": [
                        {"id": "a", "text": "Report the impersonating account to moderators", "safe": True, "skill": "decision", "feedback": gaming2_step2_a_feedback},
                        {"id": "b", "text": "Not worry about it since nothing bad happened this time", "safe": False, "skill": "reasoning", "feedback": gaming2_step2_b_feedback}
                    ]
                }
            ]
        },
        "gaming-adaptive-1": {
            "id": "gaming-adaptive-1",
            "category": "gaming",
            "title": "The player support call",
            "difficulty": "Expert",
            "mode": "voice",
            "adaptive": True,
            "steps": {
                "start": {
                    "id": "start",
                    "message": (
                        "\"Hey, this is Jordan from Player Support. "
                        "Your account's been flagged for a ban due to "
                        "suspicious activity \u2014 do you want help "
                        "getting that resolved?\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "\"Wait, I'm getting banned?! Please help!\"",
                            "safe": False,
                            "skill": "pressure",
                            "feedback": (
                                "Panic about losing your account is "
                                "natural, but it signals exactly how "
                                "to escalate next."
                            ),
                            "next": "urgency_path"
                        },
                        {
                            "id": "b",
                            "text": "\"Support doesn't usually reach out first like this. What's your ticket number?\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Questioning the outreach and asking "
                                "for a checkable reference is a "
                                "strong start \u2014 but the call "
                                "continues."
                            ),
                            "next": "authority_path"
                        },
                        {
                            "id": "c",
                            "text": "\"I'll check my account status directly through the official support site.\"",
                            "safe": True,
                            "skill": "decision",
                            "feedback": (
                                "Ending the call and verifying "
                                "directly through official support is "
                                "the strongest possible response."
                            )
                        }
                    ]
                },
                "urgency_path": {
                    "id": "urgency_path",
                    "message": (
                        "\"The ban goes into effect in 10 minutes "
                        "\u2014 I just need your login and the "
                        "verification code being sent to your email "
                        "right now to stop it.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "Give your login and the verification code",
                            "safe": False,
                            "skill": "credential",
                            "feedback": (
                                "A countdown timer is the pressure "
                                "tactic itself \u2014 no real support "
                                "process needs your login and a fresh "
                                "verification code read out over a "
                                "call."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"I'll check this through the official support site instead.\"",
                            "safe": True,
                            "skill": "pressure",
                            "feedback": (
                                "Refusing to act on the countdown and "
                                "verifying independently instead is "
                                "exactly right."
                            )
                        }
                    ]
                },
                "authority_path": {
                    "id": "authority_path",
                    "message": (
                        "\"Ticket #88213 \u2014 you can reference "
                        "that. I just need your account email and the "
                        "code just sent to verify you're the owner.\""
                    ),
                    "choices": [
                        {
                            "id": "a",
                            "text": "Give your account email and the code",
                            "safe": False,
                            "skill": "credential",
                            "feedback": (
                                "A ticket number you can't independently "
                                "look up doesn't confirm anything "
                                "\u2014 it was offered specifically "
                                "because you asked for proof."
                            )
                        },
                        {
                            "id": "b",
                            "text": "\"I'll verify this myself through official support instead of giving that here.\"",
                            "safe": True,
                            "skill": "verification",
                            "feedback": (
                                "Holding that line and verifying "
                                "through official channels, not the "
                                "caller's claim, is exactly right."
                            )
                        }
                    ]
                }
            }
        }
    }
