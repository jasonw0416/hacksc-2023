import 'dart:io';
import 'dart:async';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_sms/flutter_sms.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:telephony/telephony.dart';
import 'dart:convert';

const List<String> phoneNumber = ['8447443520'];
const double _kItemExtent = 30.0;
const List<String> _transType = <String>[
  'Driving',
  'Walking',
  'Bicycling',
  'Transit'
];
const Color mainColor = Color.fromARGB(255, 255, 85, 146);
const Color tintedWhite = Color.fromARGB(255, 57, 57, 62);
const Color darkColor = Color.fromARGB(255, 18, 12, 32);
const Color darkishColor = Color.fromARGB(255, 39, 38, 42);
void main() {
  runApp(const App());
}

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return const CupertinoApp(
      theme: CupertinoThemeData(
          brightness: Brightness.dark,
          primaryColor: mainColor,
          scaffoldBackgroundColor: darkishColor),
      home: Wrapper(),
    );
  }
}

class Wrapper extends StatefulWidget {
  const Wrapper({super.key});

  @override
  State<Wrapper> createState() => _WrapperState();
}

class _WrapperState extends State<Wrapper> {
  int _selectedTransType = 0;
  final _formKey = GlobalKey<FormState>();
  String? _receivedJson = "";
  // SmsQuery query = SmsQuery();

  TextEditingController startPointController = TextEditingController();
  TextEditingController destinationController = TextEditingController();
  final Widget _defaultDirections = Container(
    padding: const EdgeInsets.only(top: 50),
    height: 300,
    child: Image.asset(
      'assets/images/starpathlogo.png',
      // height: 50,
    ),
  );
  Widget _directions = Text('');

  parseDirections() {
    if (_receivedJson == null) {
      setState(() {
        _directions = const Text('Error in getting directions');
      });
      return;
    }

    String copyJson = _receivedJson ?? '';
    String cleanJson = copyJson
        .trim()
        .replaceFirst('Sent from your Twilio trial account - ', '');
    if (cleanJson.isEmpty) {
      setState(() {
        _directions = const Text('');
      });
      return;
    }

    var msg = json.decode(cleanJson);

    setState(() {
      _directions = Padding(
        padding: const EdgeInsets.all(25),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Row(
              children: [
                Text(
                  '${msg['t_time']}',
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(' (${msg['t_dist']})',
                    style: const TextStyle(
                      color: Colors.white54,
                    )),
              ],
            ),
            const SizedBox(
              height: 25,
            ),
            for (var step in msg['steps'])
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Text(
                    '${step['v']}',
                    style: const TextStyle(
                        fontSize: 22, fontWeight: FontWeight.bold),
                  ),
                  Text(
                    '${step['d']}',
                    style: const TextStyle(fontSize: 16, color: Colors.white54),
                  ),
                  const SizedBox(
                    height: 25,
                  ),
                ],
              ),
          ],
        ),
      );
    });
  }

  /* MESSAGE LISTENING */
  final Telephony telephony = Telephony.instance;
  void _startListening() async {
    setState(() {
      _directions = _defaultDirections;
    });
    sleep(Duration(seconds: 5));
    try {
      bool? permissionsGranted = await telephony.requestPhoneAndSmsPermissions;
      telephony.listenIncomingSms(
          onNewMessage: (SmsMessage message) {
            _receivedJson = message.body;
            parseDirections();
          },
          listenInBackground: false);
    } catch (error) {}
  }

  /* MESSAGE SENDING */
  Future<void> _pushToText(String message, List<String> recipients) async {
    try {
      if (await Permission.sms.request().isGranted) {
        String _result = await sendSMS(
          message: message,
          recipients: recipients,
          sendDirect: true,
        );
      }
    } catch (error) {
      print(error);
    }
  }

  void _showDialog(Widget child) {
    showCupertinoModalPopup<void>(
        context: context,
        builder: (BuildContext context) => Container(
              height: 150.0,
              padding: const EdgeInsets.only(top: 6.0),
              // The Bottom margin is provided to align the popup above the system navigation bar.
              margin: EdgeInsets.only(
                bottom: MediaQuery.of(context).viewInsets.bottom,
              ),
              // Provide a background color for the popup.
              color: CupertinoColors.systemBackground.resolveFrom(context),
              // Use a SafeArea widget to avoid system overlaps.
              child: SafeArea(
                top: false,
                child: child,
              ),
            ));
  }

  @override
  void initState() {
    super.initState();
    _receivedJson = "";
    _directions = _defaultDirections;
  }

  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      child: Center(
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              const SizedBox(height: 52),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: <Widget>[
                    Container(
                      decoration: BoxDecoration(
                          color: tintedWhite,
                          borderRadius: BorderRadius.circular(10)),
                      padding: const EdgeInsets.all(10),
                      child: Column(
                        children: <Widget>[
                          /* STARTING POINT */
                          CupertinoTextField.borderless(
                            placeholder: 'Starting Point',
                            controller: startPointController,
                            prefix: const Icon(
                                IconData(0xe061, fontFamily: 'MaterialIcons')),
                          ),
                          const Divider(
                            thickness: 1,
                            color: Colors.white24,
                          ),

                          /* DESTINATION */
                          CupertinoTextField.borderless(
                            placeholder: 'Destination',
                            controller: destinationController,
                            prefix: const Icon(
                                IconData(0xe3ab, fontFamily: 'MaterialIcons')),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(
                      height: 10,
                    ),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: <Widget>[
                        /* TRANSPORTATION METHOD */
                        CupertinoButton(
                          color: tintedWhite,
                          padding: const EdgeInsets.symmetric(
                            vertical: 0,
                            horizontal: 0,
                          ),
                          // Display a CupertinoPicker with list of transportation types.
                          onPressed: () => _showDialog(
                            CupertinoPicker(
                              magnification: 1.0,
                              squeeze: 1.0,
                              useMagnifier: true,
                              itemExtent: _kItemExtent,
                              // This is called when selected item is changed.
                              onSelectedItemChanged: (int selectedItem) {
                                setState(() {
                                  _selectedTransType = selectedItem;
                                });
                              },
                              children: List<Widget>.generate(_transType.length,
                                  (int index) {
                                return Center(
                                  child: Text(
                                    _transType[index],
                                  ),
                                );
                              }),
                            ),
                          ),
                          // This displays the selected destination name.
                          alignment: Alignment.centerLeft,
                          child: RichText(
                            text: TextSpan(
                              children: [
                                const WidgetSpan(
                                    alignment: PlaceholderAlignment.middle,
                                    child: Padding(
                                      padding:
                                          EdgeInsets.symmetric(horizontal: 9),
                                      child: Icon(
                                        IconData(0xe1d5,
                                            fontFamily: 'MaterialIcons'),
                                        color: mainColor,
                                      ),
                                    )),
                                TextSpan(
                                  text: _transType[_selectedTransType],
                                  style: const TextStyle(
                                    color: Colors.white,
                                    fontSize: 18,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(
                      height: 20.0,
                    ),
                  ],
                ),
              ),
              /* NAVIGATION DIRECTIONS BOX */
              Expanded(
                child: Container(
                  color: darkColor,
                  width: 100,
                  child: SingleChildScrollView(
                    child: _directions,
                  ),
                ),
              ),
              const SizedBox(height: 22),

              /* SUBMIT DIRECTIONS FORM */
              Padding(
                padding: EdgeInsets.symmetric(horizontal: 25),
                child: Container(
                  decoration: const BoxDecoration(
                      gradient: LinearGradient(
                        colors: [Color(0xff6201C3), Color(0xffDC5A84)],
                        begin: Alignment.centerLeft,
                        end: Alignment.centerRight,
                      ),
                      borderRadius: BorderRadius.all(Radius.circular(100))),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: <Widget>[
                      CupertinoButton(
                        onPressed: () {
                          // BUILD JSON
                          String json =
                              '{"start": "${startPointController.text}", "destination": "${destinationController.text}", "mode": "${_transType[_selectedTransType].toLowerCase()}"}';

                          _pushToText(json, phoneNumber);
                          _startListening();
                        },
                        child: const Text(
                          'Find Directions',
                          style: TextStyle(
                              color: Colors.white, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 22),
            ],
          ),
        ),
      ),
    );
  }
}
