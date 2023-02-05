import 'dart:async';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_sms/flutter_sms.dart';
import 'package:permission_handler/permission_handler.dart';

const List<String> phoneNumber = ['8447443520'];
const double _kItemExtent = 30.0;
const List<String> _transType = <String>[
  'Driving',
  'Walking',
  'Bicycling',
  'Transit'
];
const Color mainColor = Color.fromARGB(255, 122, 102, 255);
const Color tintedWhite = Color.fromARGB(16, 0, 0, 0);
void main() => runApp(const App());

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return const CupertinoApp(
      theme: CupertinoThemeData(
          brightness: Brightness.light, primaryColor: mainColor),
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

  TextEditingController startPointController = TextEditingController();
  TextEditingController destinationController = TextEditingController();

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
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      child: Center(
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              const SizedBox(height: 75),
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
                            color: Colors.black12,
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
                    Row(
                      children: <Widget>[
                        /* TRANSPORTATION METHOD */
                        CupertinoButton(
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
                          // prefixIcon: Icon(
                          //   IconData(0xe1d5, fontFamily: 'MaterialIcons'),
                          // ),
                          alignment: Alignment.centerLeft,
                          child: RichText(
                            text: TextSpan(
                              children: [
                                const WidgetSpan(
                                    child: Padding(
                                  padding:
                                      EdgeInsets.symmetric(horizontal: 3.0),
                                  child: Icon(
                                    IconData(0xe1d5,
                                        fontFamily: 'MaterialIcons'),
                                  ),
                                )),
                                TextSpan(
                                  text: _transType[_selectedTransType],
                                  style: const TextStyle(
                                    color: mainColor,
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
                  decoration: const BoxDecoration(
                    color: tintedWhite,
                  ),
                ),
              ),
              const SizedBox(height: 25),

              /* SUBMIT DIRECTIONS FORM */
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  CupertinoButton.filled(
                    onPressed: () {
                      // BUILD JSON
                      String json =
                          '{"start": "${startPointController.text}", "destination": "${destinationController.text}", "mode": "${_transType[_selectedTransType].toLowerCase()}"}';

                      _pushToText(json, phoneNumber);
                    },
                    child: const Text('Find Directions'),
                  ),
                ],
              ),
              const SizedBox(height: 15),
            ],
          ),
        ),
      ),
    );
  }
}
