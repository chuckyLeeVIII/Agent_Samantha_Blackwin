import React from 'react';
import {
  SafeAreaView,
  Text,
  TextInput,
  Button,
  StyleSheet,
  View,
} from 'react-native';
import config from './config.json';

export default function App() {
  const [question, setQuestion] = React.useState('');
  const [answer, setAnswer] = React.useState('');
  const [theme, setTheme] = React.useState({
    backgroundColor: '#111',
    textColor: '#eee',
  });
  const [editing, setEditing] = React.useState(false);

  const askAssistant = async () => {
    // Placeholder call to local assistant; integrate with Python backend.
    console.log('Question:', question);
    // TODO: connect to Evolve2 or other backend service
    setAnswer('Response from assistant');
  };

  return (
    <SafeAreaView
      style={[styles.container, {backgroundColor: theme.backgroundColor}]}>
      <Text style={[styles.title, {color: theme.textColor}]}>Samantha Assistant</Text>
      <TextInput
        style={[styles.input, {borderColor: theme.textColor, color: theme.textColor}]}
        placeholder="Ask a question"
        value={question}
        onChangeText={setQuestion}
      />
      <Button title="Ask" onPress={askAssistant} />
      <Text style={[styles.answer, {color: theme.textColor}]}>{answer}</Text>
      {config.allowThemeEditing && (
        editing ? (
          <View style={styles.editor}>
            <TextInput
              style={styles.input}
              placeholder="Background color"
              value={theme.backgroundColor}
              onChangeText={c => setTheme({...theme, backgroundColor: c})}
            />
            <TextInput
              style={styles.input}
              placeholder="Text color"
              value={theme.textColor}
              onChangeText={c => setTheme({...theme, textColor: c})}
            />
            <Button title="Done" onPress={() => setEditing(false)} />
          </View>
        ) : (
          <Button title="Edit Theme" onPress={() => setEditing(true)} />
        )
      )
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#111',
  },
  title: {
    fontSize: 24,
    marginBottom: 16,
    color: '#eee',
  },
  input: {
    borderWidth: 1,
    borderColor: '#555',
    padding: 8,
    marginBottom: 16,
    color: '#eee',
  },
  answer: {
    marginTop: 20,
    fontSize: 18,
    color: '#eee',
  },
  editor: {
    marginTop: 20,
  },
});
