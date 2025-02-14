# Design Patterns Project :rocket:

- **[Command](https://refactoring.guru/design-patterns/command)** 📜 - Encapsulates tasks as objects, making it easy to queue and execute tasks dynamically across peers.
- **[Strategy](https://refactoring.guru/design-patterns/strategy)** 🧠 - Manages grid search methods (e.g., Random Search, Bayesian Search) with flexibility to plug in new strategies.
- **[Singleton](https://refactoring.guru/design-patterns/singleton)** 🏠 - Ensures a single instance of the peer network configuration across the system.
- **[Facade](https://refactoring.guru/design-patterns/facade)** - Provides a simplified interface to manage complex P2P interactions and task scheduling.

## **Context**

### **What is Peer-to-Peer?** 🤝
Peer-to-peer (P2P) is a decentralized network design where nodes (peers) communicate directly with each other. There’s no central server—each peer can act as both a client and a server. This architecture makes systems more robust, scalable, and fault-tolerant.

### **What is Grid Search?** 🔍
Grid Search is a brute-force technique for **hyperparameter tuning**. It systematically tests all possible combinations of hyperparameters to find the optimal configuration for a machine learning model.

#### **Cookie-Baking Example 🍪**
Imagine you’re baking cookies and experimenting with:
- **Sugar**: 100g, 150g, 200g
- **Baking Time**: 10 mins, 15 mins, 20 mins

Grid Search will:
1. **Test all combinations**: (100g, 10 mins), (100g, 15 mins), … (200g, 20 mins).
2. **Taste each batch** 🍴 to find the perfect cookie recipe (hyperparameter set) based on flavor (model performance).

## **Installation** ⚙️

Make sure you have **Python `3.10.3`** installed. Then, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/peer-to-peer-grid-search.git
   cd peer-to-peer-grid-search
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## **Usage** 🚀

### **Starting the P2P Grid Search**

3. **Execute the grid search**:
   ```bash
   python app.py --port [PORT]
   ```

4. **Important notes**:
- The app will inform in the console when the training is finished.
- You can control possible hyperparams in the app.py file. List of possible models and params is available in file validation/possible_models_and_params.json.
- The logs of the training are stored in logger/log.text. You can also find example logs in this file, on this repository.

**For more information about the architecture, read docs.pdf file. Unfortunately, we provide only Polish version of the document for now.**



## **Why Peer-to-Peer?** 🌐

1. **Scalability**: Add or remove peers dynamically without disrupting the network.
2. **Fault Tolerance**: Tasks are redistributed if a peer fails.
3. **Efficiency**: Leverages the computational power of multiple machines.


## **Key Features** 🌟

- 🔗 **Decentralized Task Distribution**: No single point of failure.
- ⚡ **Parallel Execution**: Tasks run concurrently across peers.
- 🛠️ **Pluggable Search Strategies**: Swap or extend search methods easily.

## **License** 📜

This project is licensed under the MIT License.

