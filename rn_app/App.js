import React from 'react';
import {SafeAreaView, Text, TextInput, Button, StyleSheet} from 'react-native';

export default function App() {
  const [question, setQuestion] = React.useState('');
  const [answer, setAnswer] = React.useState('');

  const askAssistant = async () => {
    // Placeholder call to local assistant; integrate with Python backend.
    console.log('Question:', question);
    // TODO: connect to Evolve2 or other backend service
    setAnswer('Response from assistant');
  };

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Samantha Assistant</Text>
      <TextInput
        style={styles.input}
        placeholder="Ask a question"
        value={question}
        onChangeText={setQuestion}
      />
      <Button title="Ask" onPress={askAssistant} />
      <Text style={styles.answer}>{answer}</Text>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    marginBottom: 16,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 8,
    marginBottom: 16,
  },
  answer: {
    marginTop: 20,
    fontSize: 18,
  },
});
