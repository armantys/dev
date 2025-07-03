import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Camera, BarChart } from 'lucide-react';
import ImageUploader from '../components/ImageUploader';
import ConfidenceGauge from '../components/ConfidenceGauge';
import { supabase } from '../lib/supabase';

interface Prediction {
  id: string;
  label: 'PUB' | 'NO PUB';
  confidence: number;
  imageData: string;
  created_at: string;
}

const Dashboard = () => {
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadPredictions();
  }, []);

  const loadPredictions = async () => {
    try {
      const { data, error } = await supabase
        .from('predictions')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(10);

      if (error) throw error;

      setPredictions(data);
    } catch (err) {
      console.error('Error loading predictions:', err);
      setError('Failed to load predictions');
    }
  };

  const handleImageSelect = async (file: File) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Upload image to Supabase Storage
      const { data: uploadData, error: uploadError } = await supabase.storage
        .from('predictions')
        .upload(`${Date.now()}-${file.name}`, file);

      if (uploadError) throw uploadError;

      const imageUrl = supabase.storage
        .from('predictions')
        .getPublicUrl(uploadData.path).data.publicUrl;

      // Get prediction from Edge Function
      const formData = new FormData();
      formData.append('image', file);

      const response = await fetch(`${import.meta.env.VITE_SUPABASE_URL}/functions/v1/predict`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${import.meta.env.VITE_SUPABASE_ANON_KEY}`,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze image');
      }

      const result = await response.json();
      
      // Save prediction to database
      const { data: predictionData, error: predictionError } = await supabase
        .from('predictions')
        .insert({
          image_url: imageUrl,
          label: result.label.toUpperCase(),
          confidence: result.confidence,
          user_id: (await supabase.auth.getUser()).data.user?.id,
        })
        .select()
        .single();

      if (predictionError) throw predictionError;

      // Update UI
      const reader = new FileReader();
      reader.onload = () => {
        setPrediction({
          id: predictionData.id,
          label: result.label.toUpperCase() === 'PUB' ? 'PUB' : 'NO PUB',
          confidence: result.confidence,
          imageData: reader.result as string,
          created_at: predictionData.created_at,
        });
        setIsLoading(false);
        loadPredictions(); // Refresh predictions list
      };
      reader.readAsDataURL(file);
    } catch (err) {
      console.error('Error:', err);
      setError(err.message);
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <header className="mb-8">
        <h1 className="text-2xl font-bold text-gray-800 dark:text-white">
          Dashboard
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Analysez des images pour détecter la présence de publicités
        </p>
      </header>

      {error && (
        <div className="mb-6 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 p-4 rounded-lg">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Upload Section */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 transition-colors duration-200">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4 flex items-center">
            <BarChart className="w-5 h-5 mr-2 text-teal-500" />
            Analyse d'image
          </h2>
          
          <div className="space-y-6">
            <ImageUploader onImageSelect={handleImageSelect} />
            
            {isLoading && (
              <div className="flex justify-center items-center py-8">
                <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-teal-500"></div>
                <span className="ml-3 text-gray-600 dark:text-gray-400">Analyse en cours...</span>
              </div>
            )}

            <div className="flex justify-between">
              <Link
                to="/webcam"
                className="inline-flex items-center px-4 py-2 border border-teal-500 text-teal-600 dark:text-teal-400 rounded-md hover:bg-teal-50 dark:hover:bg-teal-900/20 transition-colors duration-200"
              >
                <Camera className="w-4 h-4 mr-2" />
                Utiliser la webcam
              </Link>
            </div>
          </div>
        </div>

        {/* Results Section */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 transition-colors duration-200">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
            Historique des prédictions
          </h2>
          
          <div className="space-y-4">
            {predictions.map((pred) => (
              <div key={pred.id} className="border dark:border-gray-700 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className={`font-medium ${
                    pred.label === 'PUB' ? 'text-red-500' : 'text-green-500'
                  }`}>
                    {pred.label}
                  </span>
                  <span className="text-sm text-gray-500">
                    {new Date(pred.created_at).toLocaleString()}
                  </span>
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">
                  Confiance: {pred.confidence}%
                </div>
                <img 
                  src={pred.imageData} 
                  alt={`Prediction ${pred.id}`}
                  className="mt-2 rounded-md w-full object-cover h-32"
                />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;