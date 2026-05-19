# Hospital Multi-LLM Chatbot 🏥

This project is a hospital chatbot that tries to answer questions based on hospital data.
It uses a few different language models and a simple search system to give you helpful answers.

## What it does

- Lets you chat with a hospital helper bot
- Looks for hospital info from stored text and websites
- Uses OpenAI and Hugging Face models
- Lets you compare answers from both models
- Has a Streamlit web app for easy use

## Why this is cool

I built this so the bot can:
- use existing hospital text when answering
- switch between model providers easily
- compare responses side-by-side
- show provider status in the app
- handle errors more gently

## Files you should know

- `ui.py` → Streamlit app for the web
- `app.py` → simple command-line version
- `llm_router.py` → decides which model to use
- `retriever.py` → finds the best matching text
- `embedding.py` → makes text into vectors
- `webscraping.py` → pulls hospital data from websites
- `firebase_db.py` → saves data to Firebase if needed
- `requirements.txt` → package list
- `.env` → your API keys and settings

## How to get started

### 1. Clone the project

```bash
git clone <repository-url>
cd hospital multi llm
```

### 2. Make a virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Make a `.env` file

Create a file named `.env` in the project folder and add your keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
HF_TOKEN=your_huggingface_api_key_here
```

If you want Firebase features, also add:

```env
FIREBASE_CREDENTIALS_PATH=firebase_key.json
```

## Run the app

### Best option: Streamlit UI

```bash
streamlit run ui.py
```

Then open your browser at:

`http://localhost:8501`

### Alternative: Terminal chat

```bash
python app.py
```

## How it works (simple version)

1. The bot reads hospital text and web data.
2. It turns the text into embeddings.
3. When you ask a question, it finds the most relevant text.
4. It sends that text plus your question to a model.
5. The model gives you an answer.

## Models used

- **OpenAI**: paid API, usually higher quality
- **Hugging Face**: free option, good for testing

You can choose either or compare both.

## Notes

- Keep `.venv/` for the virtual environment.
- If you have an old `venv/` folder, you can remove it.
- `requirements.txt` lists the packages needed for this project.

## Helpful tips

- If something does not work, check your `.env` keys.
- If the app says a model is unavailable, make sure the correct API key is set.
- Use `ui.py` for an easier experience.

## Dependencies

This project uses these main packages:

- `streamlit`
- `openai`
- `huggingface-hub`
- `python-dotenv`
- `beautifulsoup4`
- `langchain`
- `sentence-transformers`
- `scikit-learn`
- `numpy`
- `torch`
- `transformers`
- `firebase-admin`

See `requirements.txt` for the exact versions.


## Example Usage

### CLI Example
```
=== Hospital Chatbot ===

Choose LLM:
1. OpenAI (GPT)
2. Hugging Face (Free tier - Flan-T5)
Enter choice (1 or 2): 1

Using: openai

Ask question (type exit): What are the visiting hours?

Answer:
The hospital visiting hours are Monday to Friday from 10 AM to 7 PM, 
Saturday and Sunday from 9 AM to 8 PM. Emergency visits are allowed 24/7.
```

## Customization

### Add More Hospital Data
1. Update `webscraping.py` with new URLs
2. Run the scraper to collect data
3. Re-run `embedding.py` to regenerate embeddings
4. Restart the chatbot

### Modify System Prompt
Edit `prompt.py` to change the AI assistant's behavior, tone, or guidelines

### Adjust Retrieval Settings
In `retriever.py`, modify:
- `k=5` to change number of retrieved documents
- Embedding model in line with your needs

## Troubleshooting

### Issue: "No LLM providers available"
**Solution:** 
- Verify `.env` file exists in project root
- Check `OPENAI_API_KEY` and `HF_TOKEN` are set correctly
- Run: `python -c "from llm_router import check_llm_providers; print(check_llm_providers())"`

### Issue: "ModuleNotFoundError"
**Solution:** 
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: "OpenAI API Key Error"
**Solution:**
- Visit [OpenAI Platform](https://platform.openai.com/api-keys)
- Create new API key if expired
- Verify key has available credits
- Update `.env`: `OPENAI_API_KEY=sk-...`
- Restart Streamlit: `streamlit run ui.py`

### Issue: "Hugging Face not responding / rate limited"
**Solution:**
- Generate new token at [Hugging Face tokens](https://huggingface.co/settings/tokens)
- Verify token has inference permissions
- Update `.env`: `HF_TOKEN=hf_...`
- Check if model `google/flan-t5-base` is available and not overloaded
- Try again after a few minutes

### Issue: "Streamlit port already in use"
**Solution:**
```bash
streamlit run ui.py --server.port 8502
```

### Issue: "Empty responses or poor context"
**Solution:**
- Verify `embeddings.npy` and `texts.npy` exist
- Check `corpus_text.txt` has sufficient data
- Re-generate embeddings: `python embedding.py`
- Increase `k` in retriever.py if context is too limited

### Issue: "Virtual environment not activating"
**Solution:**
```bash
# Windows
.venv\Scripts\Activate.ps1

# If permission denied:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# macOS/Linux
source .venv/bin/activate
```

### Issue: ".venv and venv/ both exist"
**Solution:** Delete the redundant `venv/` directory
```bash
rm -r venv  # macOS/Linux
rmdir /s venv  # Windows
```
Keep only `.venv/`


## Performance Optimization

### For Speed
- ⚡ Use Hugging Face model (free, local inference in many cases)
- 🔄 Enable comparison mode only when needed (slower, two API calls)
- 📊 Reduce `k` in retriever.py for faster context retrieval

### For Accuracy
- 🎯 Use OpenAI (GPT-4o-mini) for better responses
- 🔍 Increase `k` in retriever.py (default 3, try 5-7)
- 📚 Expand knowledge base with more hospital data

### For Memory/Resources
- 💾 Use Hugging Face (smaller model footprint)
- 🔉 Reduce `MAX_NEW_TOKENS` in llm_router.py
- 📉 Limit chat history or implement persistence

### For Cost
- 💰 Use Hugging Face (free tier available)
- 🔄 Use Comparison Mode sparingly (double API calls)
- ⏱️ Set lower timeouts to prevent long-running requests


## Project Roadmap

### Completed ✅
- [x] Multi-LLM support (OpenAI + Hugging Face)
- [x] Comparison mode for quality assessment
- [x] Provider health checks
- [x] Structured error handling & logging
- [x] Streamlit UI with provider status
- [x] RAG-based context retrieval
- [x] Environment-based configuration

### In Progress 🚧
- [ ] Firebase integration for conversation history
- [ ] Enhanced prompt engineering
- [ ] Additional hospital data sources

### Future Enhancements 📋
- [ ] Multi-turn conversation memory persistence
- [ ] Real-time web scraping updates
- [ ] User feedback & rating system
- [ ] Multiple hospital support
- [ ] REST API endpoint for external integration
- [ ] Advanced analytics dashboard
- [ ] Caching layer for faster responses
- [ ] Multi-language support
- [ ] Mobile-friendly interface

## Contributing

Contributions welcome! Areas for improvement:
- Better hospital data sources & scraping
- Additional language support
- Performance optimizations
- UI/UX improvements
- Comprehensive test coverage
- Documentation improvements

**How to contribute:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## Technical Stack

- **Frontend**: Streamlit 1.28+
- **LLMs**: OpenAI GPT-4o-mini, Hugging Face Flan-T5
- **Embeddings**: SentenceTransformer (all-MiniLM-L6-v2)
- **Search**: Cosine Similarity (scikit-learn)
- **Framework**: LangChain 0.0.300+
- **Database**: Firebase Firestore (optional)
- **Languages**: Python 3.8+

## Version History

- **v1.1.0** (May 2026)
  - ✨ Comparison mode for side-by-side LLM responses
  - 🛡️ Improved error handling and logging
  - 📊 Provider health check system
  - 🎨 Enhanced Streamlit UI with sidebar
  - 📌 Pinned dependency versions

- **v1.0.0** (Initial Release)
  - Multi-LLM support
  - RAG-based retrieval
  - Web scraping pipeline
  - Embedding generation

## FAQ

**Q: Can I use this without API keys?**
A: Yes! Use only Hugging Face (free tier). OpenAI requires paid credits.

**Q: What's the difference between Comparison Mode and single models?**
A: Comparison Mode shows both OpenAI and HF responses side-by-side. Single models show one response faster.

**Q: How accurate is the context retrieval?**
A: Accuracy depends on your knowledge base quality and k parameter. Better data = better results.

**Q: Can I run this locally without APIs?**
A: Partially. You can use local Hugging Face models, but you'll need to modify the code.

**Q: How do I update the knowledge base?**
A: 1) Update `webscraping.py` with new URLs, 2) Run it, 3) Re-run `embedding.py`

## Support & Documentation

- 📖 [OpenAI API Docs](https://platform.openai.com/docs)
- 🤗 [Hugging Face Docs](https://huggingface.co/docs)
- 🌊 [Streamlit Docs](https://docs.streamlit.io)
- 🔗 [LangChain Docs](https://python.langchain.com/)

## License

[Specify your license here - e.g., MIT, Apache 2.0, GPL 3.0]

## Acknowledgments

- Hospital data sourced from public websites
- Built with LangChain and Sentence Transformers
- LLM providers: OpenAI and Hugging Face
- Embedding model: all-MiniLM-L6-v2 (maintained by SBERT)

---

**Made with ❤️ for hospital information assistance | Last Updated: May 2026**

