# Model Providers

## Google AI (Gemini)

```go
import "github.com/genkit-ai/genkit/go/plugins/googlegenai"

g := genkit.Init(ctx, genkit.WithPlugins(&googlegenai.GoogleAI{}))
```

**Env var:** `GEMINI_API_KEY` or `GOOGLE_API_KEY`

Model names follow the format `googleai/<model-id>`. Look up the latest model IDs at https://ai.google.dev/gemini-api/docs/models.

```go
// By name string
ai.WithModelName("googleai/gemini-flash-latest")

// Model ref with provider-specific config
ai.WithModel(googlegenai.ModelRef("googleai/gemini-flash-latest", &genai.GenerateContentConfig{
	ThinkingConfig: &genai.ThinkingConfig{
		ThinkingBudget: genai.Ptr[int32](0), // disable thinking
	},
}))

// Lookup a model instance
m := googlegenai.GoogleAIModel(g, "gemini-flash-latest")
```

## Vertex AI

```go
import "github.com/genkit-ai/genkit/go/plugins/googlegenai"

g := genkit.Init(ctx, genkit.WithPlugins(&googlegenai.VertexAI{}))
```

**Env vars:** `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION` (or `GOOGLE_CLOUD_REGION`)

Uses Application Default Credentials (`gcloud auth application-default login`).

Model names follow the format `vertexai/<model-id>`. Same model IDs as Google AI.

```go
ai.WithModelName("vertexai/gemini-flash-latest")
```

## OpenAI-Compatible (compat_oai)

Works with any OpenAI-compatible API: OpenAI, DeepSeek, xAI, etc.

```go
import "github.com/genkit-ai/genkit/go/plugins/compat_oai"

openaiPlugin := &compat_oai.OpenAICompatible{
	Provider: "openai",   // unique identifier
	APIKey:   os.Getenv("OPENAI_API_KEY"),
	// BaseURL: "https://custom-endpoint/v1", // for non-OpenAI providers
}
g := genkit.Init(ctx, genkit.WithPlugins(openaiPlugin))
```

Define models explicitly (not auto-discovered):

```go
model := openaiPlugin.DefineModel("openai", "gpt-4o", compat_oai.ModelOptions{})
```

Use with:
```go
ai.WithModel(model)
```

## Ollama

```go
import "github.com/genkit-ai/genkit/go/plugins/ollama"

g := genkit.Init(ctx, genkit.WithPlugins(&ollama.Ollama{
	ServerAddress: "http://localhost:11434", // optional, this is the default
}))
```

Define models:

```go
model := ollama.DefineModel(g, "llama3.2", ollama.ModelOptions{})
ai.WithModel(model)
```

## Multiple Providers

Register multiple plugins in a single Genkit instance:

```go
g := genkit.Init(ctx,
	genkit.WithPlugins(
		&googlegenai.GoogleAI{},
		&vertexai.VertexAI{},
	),
	genkit.WithDefaultModel("googleai/gemini-flash-latest"),
)

// Use different models per call
text1, _ := genkit.GenerateText(ctx, g,
	ai.WithModelName("googleai/gemini-flash-latest"),
	ai.WithPrompt("Hello from Gemini Google AI"),
)

text2, _ := genkit.GenerateText(ctx, g,
	ai.WithModelName("vertexai/gemini-flash-latest"),
	ai.WithPrompt("Hello from Gemini Vertex AI"),
)
```
