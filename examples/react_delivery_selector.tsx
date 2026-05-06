/**
 * React component for CDEK delivery service selection
 *
 * This component demonstrates how to use the FastAPI backend
 * with CDEK reference data to build a delivery configuration UI.
 */

import React, { useState, useEffect } from 'react';

// Types
interface Service {
  code: string;
  name: string;
  description: string;
  modes?: string[];
  weight_limit?: number;
  requires_parameter?: boolean;
  restrictions?: string;
}

interface BoxSuggestion {
  code: string;
  name: string;
  dimensions?: string;
  max_weight?: number;
  description: string;
}

interface DeliveryWizardResponse {
  suggested_box: BoxSuggestion | null;
  recommended_services: Service[];
  all_available_services: Array<{ code: string; name: string }>;
}

// Main component
export function DeliveryServiceSelector() {
  const [weight, setWeight] = useState<number>(1.0);
  const [mode, setMode] = useState<string>('warehouse-door');
  const [isEcommerce, setIsEcommerce] = useState<boolean>(true);

  const [wizard, setWizard] = useState<DeliveryWizardResponse | null>(null);
  const [selectedServices, setSelectedServices] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch delivery wizard recommendations
  useEffect(() => {
    if (weight <= 0) return;

    const timer = setTimeout(async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(
          `/api/delivery-wizard?weight=${weight}&mode=${mode}&is_ecommerce=${isEcommerce}`
        );

        if (!response.ok) {
          throw new Error('Failed to fetch recommendations');
        }

        const data = await response.json();
        setWizard(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    }, 500); // debounce

    return () => clearTimeout(timer);
  }, [weight, mode, isEcommerce]);

  const toggleService = (code: string) => {
    setSelectedServices(prev =>
      prev.includes(code)
        ? prev.filter(c => c !== code)
        : [...prev, code]
    );
  };

  return (
    <div className="delivery-selector">
      <h2>Настройка доставки СДЭК</h2>

      {/* Weight and mode inputs */}
      <div className="form-group">
        <label>
          Вес посылки (кг):
          <input
            type="number"
            value={weight}
            onChange={(e) => setWeight(parseFloat(e.target.value))}
            min="0.1"
            step="0.1"
          />
        </label>
      </div>

      <div className="form-group">
        <label>
          Режим доставки:
          <select value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="warehouse-warehouse">Склад - Склад</option>
            <option value="warehouse-door">Склад - Дверь</option>
            <option value="door-door">Дверь - Дверь</option>
            <option value="warehouse-postamat">Склад - Постамат</option>
          </select>
        </label>
      </div>

      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={isEcommerce}
            onChange={(e) => setIsEcommerce(e.target.checked)}
          />
          Интернет-магазин
        </label>
      </div>

      {/* Loading state */}
      {loading && <div className="loading">Загрузка рекомендаций...</div>}

      {/* Error state */}
      {error && <div className="error">{error}</div>}

      {/* Suggested box */}
      {wizard?.suggested_box && (
        <div className="suggested-box">
          <h3>Рекомендуемая упаковка</h3>
          <div className="box-card">
            <strong>{wizard.suggested_box.name}</strong>
            {wizard.suggested_box.dimensions && (
              <p>Размеры: {wizard.suggested_box.dimensions} см</p>
            )}
            {wizard.suggested_box.max_weight && (
              <p>Максимальный вес: {wizard.suggested_box.max_weight} кг</p>
            )}
            <p className="description">{wizard.suggested_box.description}</p>
          </div>
        </div>
      )}

      {/* Recommended services */}
      {wizard?.recommended_services && wizard.recommended_services.length > 0 && (
        <div className="recommended-services">
          <h3>Рекомендуемые услуги</h3>
          {wizard.recommended_services.map((service) => (
            <div key={service.code} className="service-card">
              <label>
                <input
                  type="checkbox"
                  checked={selectedServices.includes(service.code)}
                  onChange={() => toggleService(service.code)}
                />
                <div className="service-info">
                  <strong>{service.name}</strong>
                  <p>{service.description}</p>
                  {service.restrictions && (
                    <p className="restrictions">
                      <small>⚠️ {service.restrictions}</small>
                    </p>
                  )}
                </div>
              </label>
            </div>
          ))}
        </div>
      )}

      {/* All available services */}
      {wizard?.all_available_services && (
        <details className="all-services">
          <summary>
            Все доступные услуги ({wizard.all_available_services.length})
          </summary>
          <div className="services-list">
            {wizard.all_available_services.map((service) => (
              <label key={service.code} className="service-item">
                <input
                  type="checkbox"
                  checked={selectedServices.includes(service.code)}
                  onChange={() => toggleService(service.code)}
                />
                {service.name}
              </label>
            ))}
          </div>
        </details>
      )}

      {/* Selected services summary */}
      {selectedServices.length > 0 && (
        <div className="selected-summary">
          <h3>Выбрано услуг: {selectedServices.length}</h3>
          <ul>
            {selectedServices.map((code) => (
              <li key={code}>{code}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

// Service details modal component
export function ServiceDetailsModal({ serviceCode }: { serviceCode: string }) {
  const [service, setService] = useState<Service | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetch(`/api/services/${serviceCode}`)
      .then(res => res.json())
      .then(data => {
        setService(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load service details:', err);
        setLoading(false);
      });
  }, [serviceCode]);

  if (loading) return <div>Загрузка...</div>;
  if (!service) return <div>Услуга не найдена</div>;

  return (
    <div className="service-modal">
      <h2>{service.name}</h2>
      <p>{service.description}</p>

      {service.modes && (
        <div>
          <strong>Доступные режимы:</strong>
          <ul>
            {service.modes.map(mode => (
              <li key={mode}>{mode}</li>
            ))}
          </ul>
        </div>
      )}

      {service.weight_limit && (
        <p><strong>Ограничение по весу:</strong> {service.weight_limit} кг</p>
      )}

      {service.restrictions && (
        <div className="restrictions">
          <strong>Ограничения:</strong>
          <p>{service.restrictions}</p>
        </div>
      )}
    </div>
  );
}

// Packaging selector component
export function PackagingSelector({ weight, mode }: { weight: number; mode: string }) {
  const [suggestion, setSuggestion] = useState<BoxSuggestion | null>(null);
  const [allPackaging, setAllPackaging] = useState<Service[]>([]);

  useEffect(() => {
    // Get suggestion
    fetch(`/api/packaging/suggest?weight=${weight}&mode=${mode}`)
      .then(res => res.json())
      .then(data => setSuggestion(data))
      .catch(() => setSuggestion(null));

    // Get all packaging options
    fetch('/api/packaging')
      .then(res => res.json())
      .then(data => setAllPackaging(data));
  }, [weight, mode]);

  return (
    <div className="packaging-selector">
      {suggestion && (
        <div className="suggestion">
          <h3>💡 Рекомендуем</h3>
          <div className="box-highlight">
            <strong>{suggestion.name}</strong>
            {suggestion.dimensions && <p>📦 {suggestion.dimensions} см</p>}
            {suggestion.max_weight && <p>⚖️ До {suggestion.max_weight} кг</p>}
          </div>
        </div>
      )}

      <div className="all-packaging">
        <h3>Все варианты упаковки</h3>
        <div className="packaging-grid">
          {allPackaging.map((pkg) => (
            <div key={pkg.code} className="packaging-card">
              <strong>{pkg.name}</strong>
              <p>{pkg.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
